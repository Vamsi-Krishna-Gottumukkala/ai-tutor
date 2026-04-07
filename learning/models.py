from django.db import models
from accounts.models import User
from subjects.models import Subject


class LearningPath(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='learning_paths')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='learning_paths')
    recommendations = models.JSONField(default=list)
    important_questions = models.JSONField(default=list)
    study_tips = models.JSONField(default=list)
    generated_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'subject']
        ordering = ['-updated_at']

    def __str__(self):
        return f"Learning Path: {self.user.email} | {self.subject.name}"


class Flashcard(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='flashcards')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='flashcards')
    topic = models.CharField(max_length=200)
    front_text = models.TextField()  # Concept / Question
    back_text = models.TextField()   # Explanation / Answer
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['topic', 'created_at']

    def __str__(self):
        return f"[{self.topic}] {self.front_text[:50]}"


class DailyQuiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_quizzes')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='daily_quizzes')
    scheduled_date = models.DateField()
    quiz = models.ForeignKey('assessments.Quiz', on_delete=models.SET_NULL, null=True, blank=True)
    is_locked = models.BooleanField(default=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ['user', 'subject', 'scheduled_date']
        ordering = ['-scheduled_date']

    def __str__(self):
        return f"Daily Quiz: {self.user.email} | {self.subject.name} | {self.scheduled_date}"
