from django.urls import path
from . import views

app_name = 'assessments'

urlpatterns = [
    path('start/<int:subject_id>/', views.start_basic_quiz, name='start_basic_quiz'),
    path('quiz/<int:quiz_id>/', views.take_quiz, name='take_quiz'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz, name='submit_quiz'),
    path('results/<int:attempt_id>/', views.quiz_results, name='quiz_results'),
    path('history/', views.quiz_history, name='history'),
]
