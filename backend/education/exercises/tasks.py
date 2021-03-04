import random
import time

from typing import Tuple
from celery import shared_task
from django.db.models import Q
from .models import ExerciseReviewStatus, Exercise, ExerciseReply

@shared_task
def check_review_status() -> str:
    REVIEW_STATUSES = {status.slug: status for status in ExerciseReviewStatus.objects.all()}
    replies = ExerciseReply.objects.filter(Q(service_id=None) | Q(status=REVIEW_STATUSES['evaluation']))
    cnt_changed = 0
    for reply in replies:
        _, status = get_submission(reply.service_id)
        if (status in REVIEW_STATUSES and status != reply.status.slug):
            cnt_changed += 1
            reply.status = REVIEW_STATUSES[status]
            reply.save()

    return "Обработано: %s, из них обновлен статус: %s" % (len(replies), cnt_changed)


@shared_task
def send_for_review(reply_id: int) -> str:
    reply = ExerciseReply.objects.get(id=reply_id)
    id, status = post_submission(reply.reply_text)
    reply.service_id = id
    reply.save()
    
    return "Review service_id: %s, status: %s" % (id, status)


def post_submission(reply: str) -> Tuple[int, str]:
    id = int(time.time() * 1000)
    status = random.choice([*['evaluation'] * 10, 'correct', 'wrong'])

    return id, status

def get_submission(id: int) -> Tuple[int, str]:
    status = random.choice([*['evaluation'] * 10, 'correct', 'wrong'])

    return id, status
