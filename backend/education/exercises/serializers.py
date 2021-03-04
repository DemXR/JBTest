from rest_framework import serializers
from .models import Exercise, ExerciseReview, ExerciseReply, ExerciseReviewStatus


class ExerciseSerializer(serializers.Serializer):
    """
        Упражнения
    """
    class Meta:
        model = Exercise

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=True, max_length=128)
    body = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(required=True)

    def create(self, validated_data):
        return Exercise.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.code)
        instance.save()
        return instance

class ExerciseReviewStatusSerializer(serializers.Serializer):
    """
        Статусы ревью
    """
    class Meta:
        model = ExerciseReviewStatus

    slug = serializers.CharField()
    name = serializers.CharField()


class ExerciseReplySerializer(serializers.Serializer):
    """
        Ответы на упражнения
    """
    class Meta:
        model = ExerciseReply

    reply_text = serializers.CharField()
    status = ExerciseReviewStatusSerializer()


class ExerciseReviewSerializer(serializers.Serializer):
    """
        Запросы на ревью
    """
    class Meta:
        model = ExerciseReview

    id = serializers.IntegerField(read_only=True)
    reply = ExerciseReplySerializer(read_only=True)
    created_at = serializers.DateTimeField
