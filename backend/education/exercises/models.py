import hashlib

from django.db import models
from django.contrib.sessions.models import Session

class ExerciseReviewStatus(models.Model):
    """
        Статусы ревью
    """
    class Meta:
        # "d_" означает "dictionary". Данная таблица содержит редко изменяемую справочную информацию.
        db_table = "d_exercises_replies_statuses"

    slug = models.CharField(max_length=64, unique=True, help_text="Текстовый идентификатор статуса проверки упражнения")
    name = models.CharField(max_length=128, help_text="Наименование статуса проверки упражнения")

    def __str__(self):
        return self.name
        

class Exercise(models.Model):
    """
        Упражнения
    """
    class Meta:
        db_table = "exercises"
        ordering = ["id"]

    title = models.CharField(max_length=128, help_text="Заголовок упражнения")
    body = models.TextField(help_text="Подробное описание упражнения")
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ExerciseReply(models.Model):
    """
        Ответы на упражнения
    """
    class Meta:
        db_table = "exercises_replies"
        unique_together = ('exercise', 'reply_hash')
    
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, help_text="Идентификатор упражнения")
    reply_hash = models.TextField(blank=True, help_text="Хэш-сумма тела ответа")
    reply_text = models.TextField(help_text="Текст выполнения упражнения")
    service_id = models.BigIntegerField(null=True, help_text="Идентификатор проверки из внешнего сервиса проверки")
    status = models.ForeignKey(ExerciseReviewStatus, on_delete=models.DO_NOTHING, default=1)
    created_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.reply_text


class ExerciseReview(models.Model):
    """
        Запросы на ревью
    """

    class Meta:
        db_table = "exercises_reviews"
        ordering = ["-created_at"]

    exercise = models.ForeignKey(Exercise, related_name='reviews', on_delete=models.CASCADE, help_text="Идентификатор упражнения")
    reply = models.ForeignKey(ExerciseReply, related_name="Exercise", on_delete=models.CASCADE, help_text="Идентификатор ответа")
    session_id = models.CharField(max_length=32, db_index=True, help_text="Сессия пользователя")  
    created_at = models.DateTimeField(auto_now=True)

    @classmethod
    def create(cls, exercise: Exercise, reply_text: str, session_id: str) -> models.Model:
        reply_hash = hashlib.md5(reply_text.encode('utf-8')).hexdigest()
        reply, created = ExerciseReply.objects.get_or_create(exercise=exercise, reply_hash=reply_hash, reply_text=reply_text)
        review = cls(exercise=exercise, reply=reply, session_id=session_id)

        return review
