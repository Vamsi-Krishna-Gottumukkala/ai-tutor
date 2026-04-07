from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    SKILL_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]
    email = models.EmailField(unique=True)
    skill_level = models.CharField(max_length=20, choices=SKILL_LEVELS, default='beginner')
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email

    @property
    def display_name(self):
        return self.get_full_name() or self.username or self.email.split('@')[0]

    @property
    def skill_level_display(self):
        return self.get_skill_level_display()
