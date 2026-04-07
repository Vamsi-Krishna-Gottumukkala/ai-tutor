from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('users/', views.manage_users, name='users'),
    path('users/<int:user_id>/toggle/', views.toggle_user_active, name='toggle_user'),
    path('users/<int:user_id>/delete/', views.delete_user, name='delete_user'),
    path('subjects/', views.manage_subjects, name='subjects'),
    path('subjects/<int:subject_id>/delete/', views.delete_subject, name='delete_subject'),
    path('quizzes/', views.view_quizzes, name='quizzes'),
    path('performance/', views.student_performance, name='performance'),
    path('moderation/', views.content_moderation, name='moderation'),
    path('moderation/<int:message_id>/delete/', views.delete_chat_message, name='delete_message'),
]
