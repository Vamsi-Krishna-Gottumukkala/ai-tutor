from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='list'),
    path('create/', views.create_subject, name='create'),
    path('<int:pk>/', views.subject_detail, name='detail'),
    path('<int:pk>/delete/', views.delete_subject, name='delete'),
]
