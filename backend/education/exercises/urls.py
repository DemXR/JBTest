from .views import getExercisesList, getExercisesById, exercise_review, getReviewResult
from django.urls import path

urlpatterns = [
    path('', getExercisesList),
    path('<int:exercise_id>/', getExercisesById),
    path('<int:exercise_id>/review/', exercise_review),
    path('<int:exercise_id>/review/<int:review_id>/', getReviewResult),
]