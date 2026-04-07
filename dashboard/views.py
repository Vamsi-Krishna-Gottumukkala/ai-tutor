from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from subjects.models import Subject
from assessments.models import QuizAttempt, WeakTopic
from learning.models import LearningPath, Flashcard


@login_required
def home(request):
    if request.user.is_staff:
        return redirect('admin_panel:dashboard')

    subjects = Subject.objects.filter(owner=request.user)
    recent_attempts = QuizAttempt.objects.filter(
        user=request.user
    ).select_related('quiz__subject').order_by('-attempt_date')[:5]

    # For charts: score history (last 10)
    all_attempts = QuizAttempt.objects.filter(
        user=request.user
    ).order_by('attempt_date')[:10]

    score_labels = [a.quiz.subject.name[:10] for a in all_attempts]
    score_data = [a.percentage for a in all_attempts]

    # Overall stats
    total_attempts = QuizAttempt.objects.filter(user=request.user).count()
    avg_score = 0
    if total_attempts:
        avg_score = sum(a.percentage for a in QuizAttempt.objects.filter(user=request.user)) / total_attempts

    weak_topics = WeakTopic.objects.filter(user=request.user).order_by('-miss_count')[:5]

    context = {
        'subjects': subjects,
        'recent_attempts': recent_attempts,
        'score_labels': score_labels,
        'score_data': score_data,
        'total_attempts': total_attempts,
        'avg_score': round(avg_score, 1),
        'weak_topics': weak_topics,
        'skill_level': request.user.skill_level,
    }
    return render(request, 'dashboard/dashboard.html', context)
