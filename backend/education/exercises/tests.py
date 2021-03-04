from django.test import TestCase
from rest_framework.test import APIClient
from .models import Exercise, ExerciseReviewStatus
import json

class ExerciseTests(TestCase):
    """
        Тестирование приложения "Решение задач на код"
    """

    def setUp(self):
        self.client = APIClient()
        _ = ExerciseReviewStatus.objects.create(slug='evaluation', name='На проверке')
        _ = ExerciseReviewStatus.objects.create(slug='wrong', name='Неверно')
        _ = ExerciseReviewStatus.objects.create(slug='correct', name='Верно')
        exercise = Exercise.objects.create(title='TestTitle', body='TestBody')

    def tearDown(self):
        self.client.logout()

    def test_review(self):
        # Запрос перечня упражнений
        response = self.client.get('/api/exercise/')
        self.assertEqual(response.status_code, 200)

        exercises = json.loads(response.content.decode('utf-8'))
        self.assertGreater(len(exercises), 0)

        # Отправка ответа на ревью
        exercise = exercises[0]
        url = '/api/exercise/%s/review/' % exercise.get('id')
        body = {'reply': 'print("hello, world!")'}
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 201)

        review = json.loads(response.content.decode('utf-8'))
        self.assertGreater(review.get('id'), 0)
        
        status_slug = review.get('reply').get('status').get('slug')
        self.assertIn(status_slug, ['evaluation', 'wrong', 'correct'])

        # Запрос результата ревью по коду ревью
        url = '/api/exercise/%s/review/%s/' % (exercise.get('id'), review.get('id'))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

        review = json.loads(response.content.decode('utf-8'))
        self.assertGreater(review.get('id'), 0)
        
        status_slug = review.get('reply').get('status').get('slug')
        self.assertIn(status_slug, ['evaluation', 'wrong', 'correct'])