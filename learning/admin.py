from django.contrib import admin
from .models import LearningPath, Flashcard, DailyQuiz

@admin.register(Flashcard)
class FlashcardAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject', 'topic', 'created_at']
