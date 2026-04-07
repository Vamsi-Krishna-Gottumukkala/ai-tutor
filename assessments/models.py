from django.db import models
from accounts.models import User
from subjects.models import Subject


class Quiz(models.Model):
    QUIZ_TYPES = [('basic', 'Basic Test'), ('daily', 'Daily Quiz')]
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='quizzes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='quizzes')
    quiz_type = models.CharField(max_length=10, choices=QUIZ_TYPES, default='basic')
    generated_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-generated_at']

    def __str__(self):
        return f"{self.get_quiz_type_display()} | {self.subject.name} | {self.user.email}"

    @property
    def total_questions(self):
        return self.questions.count()


class Question(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_answer = models.CharField(max_length=1)  # 'a', 'b', 'c', or 'd'
    topic_tag = models.CharField(max_length=200, blank=True)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def get_options(self):
        return {
            'a': self.option_a,
            'b': self.option_b,
            'c': self.option_c,
            'd': self.option_d,
        }


class QuizAttempt(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='attempts')
    score = models.IntegerField(default=0)
    total_questions = models.IntegerField(default=10)
    percentage = models.FloatField(default=0.0)
    skill_level = models.CharField(max_length=20, default='beginner')
    answers = models.JSONField(default=dict)  # {str(question_id): selected_option}
    attempt_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-attempt_date']

    def __str__(self):
        return f"{self.user.email} | {self.quiz.subject.name} | {self.percentage:.1f}%"


class WeakTopic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weak_topics')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='weak_topics')
    topic_name = models.CharField(max_length=200)
    miss_count = models.IntegerField(default=1)

    class Meta:
        unique_together = ['user', 'subject', 'topic_name']
        ordering = ['-miss_count']

    def __str__(self):
        return f"{self.topic_name} (missed {self.miss_count}x)"
