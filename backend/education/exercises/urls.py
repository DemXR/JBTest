from .views import getExercisesList, getExercisesById, exercise_review, getReviewResult
from django.urls import path

urlpatterns = [
    path('', getExercisesList),  # Список упражненией
    path('<int:exercise_id>/', getExercisesById),  # Сведения об упражнении по id упражнения
    path('<int:exercise_id>/review/', exercise_review),  # Отправка результата на ревью + запрос всех ревью
    path('<int:exercise_id>/review/<int:review_id>/', getReviewResult),  # Сведения о результатах по id результата
]