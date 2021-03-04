from django.contrib import admin
from .models import Exercise, ExerciseReviewStatus, ExerciseReview, ExerciseReply

class ExerciseReviewAdmin(admin.ModelAdmin):
    list_display = ('exercise', 'reply', 'status', 'created_at')
    list_filter = ('reply__status', ('created_at', admin.DateFieldListFilter),)
    raw_id_admin = ('reply', )

    def status(self, obj):
        return obj.reply.status
    status.short_description = 'Status'
    status.admin_order_field = 'reply__status__name'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(Exercise)
admin.site.register(ExerciseReview, ExerciseReviewAdmin)
