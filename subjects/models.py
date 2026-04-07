from django.db import models
from accounts.models import User


class Subject(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subjects')
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    syllabus_text = models.TextField(blank=True)
    syllabus_pdf = models.FileField(upload_to='syllabi/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.owner.email})"

    @property
    def has_basic_test_completed(self):
        from assessments.models import QuizAttempt
        return QuizAttempt.objects.filter(
            user=self.owner,
            quiz__subject=self,
            quiz__quiz_type='basic'
        ).exists()

    @property
    def latest_attempt(self):
        from assessments.models import QuizAttempt
        return QuizAttempt.objects.filter(
            user=self.owner,
            quiz__subject=self
        ).order_by('-attempt_date').first()

    @property
    def topic_list(self):
        return list(self.topics.values_list('topic_name', flat=True))


class SyllabusTopic(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='topics')
    topic_name = models.CharField(max_length=200)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.topic_name
