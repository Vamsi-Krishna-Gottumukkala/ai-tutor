from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg, Count
from accounts.models import User
from subjects.models import Subject
from assessments.models import Quiz, QuizAttempt, Question, WeakTopic
from chatbot.models import ChatMessage
from .decorators import admin_required


@admin_required
def dashboard(request):
    total_users = User.objects.filter(is_staff=False).count()
    total_subjects = Subject.objects.count()
    total_quizzes = Quiz.objects.count()
    total_attempts = QuizAttempt.objects.count()

    avg_score = QuizAttempt.objects.aggregate(avg=Avg('percentage'))['avg'] or 0

    level_counts = {
        'beginner': User.objects.filter(skill_level='beginner', is_staff=False).count(),
        'intermediate': User.objects.filter(skill_level='intermediate', is_staff=False).count(),
        'advanced': User.objects.filter(skill_level='advanced', is_staff=False).count(),
    }

    recent_attempts = QuizAttempt.objects.select_related(
        'user', 'quiz__subject'
    ).order_by('-attempt_date')[:10]

    return render(request, 'admin_panel/dashboard.html', {
        'total_users': total_users,
        'total_subjects': total_subjects,
        'total_quizzes': total_quizzes,
        'total_attempts': total_attempts,
        'avg_score': round(avg_score, 1),
        'level_counts': level_counts,
        'recent_attempts': recent_attempts,
    })


@admin_required
def manage_users(request):
    users = User.objects.filter(is_staff=False).order_by('-date_joined')
    return render(request, 'admin_panel/users.html', {'users': users})


@admin_required
def toggle_user_active(request, user_id):
    user = get_object_or_404(User, pk=user_id, is_staff=False)
    user.is_active = not user.is_active
    user.save()
    status = 'activated' if user.is_active else 'blocked'
    messages.success(request, f'User {user.email} has been {status}.')
    return redirect('admin_panel:users')


@admin_required
def delete_user(request, user_id):
    user = get_object_or_404(User, pk=user_id, is_staff=False)
    if request.method == 'POST':
        email = user.email
        user.delete()
        messages.success(request, f'User {email} deleted successfully.')
    return redirect('admin_panel:users')


@admin_required
def manage_subjects(request):
    subjects = Subject.objects.select_related('owner').order_by('-created_at')
    return render(request, 'admin_panel/subjects.html', {'subjects': subjects})


@admin_required
def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == 'POST':
        name = subject.name
        subject.delete()
        messages.success(request, f'Subject "{name}" deleted.')
    return redirect('admin_panel:subjects')


@admin_required
def view_quizzes(request):
    quizzes = Quiz.objects.select_related('subject', 'user').order_by('-generated_at')
    return render(request, 'admin_panel/quizzes.html', {'quizzes': quizzes})


@admin_required
def student_performance(request):
    attempts = QuizAttempt.objects.select_related(
        'user', 'quiz__subject'
    ).order_by('-attempt_date')

    # Filters
    level_filter = request.GET.get('level', '')
    if level_filter:
        attempts = attempts.filter(skill_level=level_filter)

    return render(request, 'admin_panel/performance.html', {
        'attempts': attempts,
        'level_filter': level_filter,
    })


@admin_required
def content_moderation(request):
    flagged_messages = ChatMessage.objects.select_related(
        'session__user', 'session__subject'
    ).filter(role='user').order_by('-timestamp')[:100]

    return render(request, 'admin_panel/moderation.html', {
        'messages': flagged_messages,
    })


@admin_required
def delete_chat_message(request, message_id):
    msg = get_object_or_404(ChatMessage, pk=message_id)
    if request.method == 'POST':
        msg.delete()
        messages.success(request, 'Message deleted.')
    return redirect('admin_panel:moderation')
