from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.request import Request
from .models import Exercise, ExerciseReview
from .serializers import ExerciseSerializer, ExerciseReviewSerializer
from .tasks import send_for_review


@api_view(["GET"])
@permission_classes((AllowAny,))
def getExercisesList(request: Request) -> Response:
    """
        Метод возвращает перечень упражнений
    """
    if not request.session or not request.session.session_key:
        request.session.save()
        
    exercises = Exercise.objects.all()
    result = []
    for exercise in exercises:
        serialized_exercise = ExerciseSerializer(exercise).data

        # Если текущий пользователь уже отправлял на ревью, то возвращается результат ревью
        if request.session and request.session.session_key:
            try:
                review = ExerciseReview.objects.filter(exercise=exercise, session_id=request.session.session_key).first()
                serialized_review = ExerciseReviewSerializer(review).data
                serialized_exercise['review'] = serialized_review
            except ObjectDoesNotExist:
                pass
        result.append(serialized_exercise)

    return Response(result, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes((AllowAny,))
def getExercisesById(request: Request, exercise_id: int) -> Response:
    """
        Метод возвращает сведения об упражнении по его id
    """
    try:
        exercise = Exercise.objects.get(id=exercise_id)
        serialized_exercise = ExerciseSerializer(exercise).data

        return Response(serialized_exercise, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(None, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST", "GET"])
@permission_classes((AllowAny,))
"""
    Если метод POST, то отправляет ответ на review;
    Если метод GET, то запрашивает результат последнего review.
"""
def exercise_review(request: Request, exercise_id: int) -> Response:
    if request.method == 'POST':
        return sendReplyForReview(request, exercise_id)
    else:
        return getReviewInfo(request, exercise_id)

def getReviewInfo(request: Request, exercise_id: int) -> Response:
    if not request.session or not request.session.session_key:
        return Response({}, status=status.HTTP_204_NO_CONTENT)
    else:
        session_id = request.session.session_key
        review = ExerciseReview.objects.filter(session_id=session_id)
        if (len(review) > 0):
            serialized_exercise = ExerciseReviewSerializer(review[0]).data
            return Response(serialized_exercise, status=status.HTTP_200_OK)
        else:
            return Response({}, status=status.HTTP_204_NO_CONTENT)


def sendReplyForReview(request: Request, exercise_id: int) -> Response:
    if not request.session or not request.session.session_key:
        request.session.save()

    session_id = request.session.session_key
    reply_text = request.data.get('reply')

    if not reply_text:
        return Response({"details": "Отсутствует атрибут '%s'" % "reply"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    if not (isinstance(reply_text, str)):
        return Response({"details": "Значение атрибута '%s' должно быть строкового типа." % "reply"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    try:
        exercise = Exercise.objects.get(id=exercise_id)
    except ObjectDoesNotExist:
        return Response({"details": "Упражнение (id=%s) не найдено." % exercise_id}, status=status.HTTP_404_NOT_FOUND)
    else:
        review = ExerciseReview.create(exercise=exercise, reply_text=reply_text, session_id=session_id)
        review.save()

        if review.reply.status.slug == 'evaluation':
            send_for_review.s(review.reply.id).apply_async()
            
        serialized_exercise = ExerciseReviewSerializer(review).data
        return Response(serialized_exercise, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes((AllowAny,))
def getReviewResult(request: Request, exercise_id: int, review_id: int) -> Response:
    """
        Запрос результа ревью по его id
    """
    try:
        review = ExerciseReview.objects.get(id=review_id, session_id=request.session.session_key)
        serialized_review = ExerciseReviewSerializer(review).data
        return Response(serialized_review, status=status.HTTP_200_OK)
    except ObjectDoesNotExist:
        return Response(None, status=status.HTTP_404_NOT_FOUND)

