from django.contrib import admin
from .models import Quiz, Question, QuizAttempt, WeakTopic

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['subject', 'user', 'quiz_type', 'is_completed', 'generated_at']

@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'quiz', 'score', 'percentage', 'skill_level', 'attempt_date']
