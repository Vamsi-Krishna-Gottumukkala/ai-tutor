from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('path/<int:subject_id>/', views.learning_path, name='learning_path'),
    path('flashcards/<int:subject_id>/', views.flashcards, name='flashcards'),
    path('daily/<int:subject_id>/', views.daily_quiz_home, name='daily_quiz'),
]
