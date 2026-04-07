from django.urls import path
from . import views

app_name = 'chatbot'

urlpatterns = [
    path('', views.chat_page, name='chat'),
    path('<int:subject_id>/', views.chat_page, name='chat_subject'),
    path('api/send/', views.send_message, name='send_message'),
]
