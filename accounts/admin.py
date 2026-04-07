from django.contrib import admin
from .models import User

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'skill_level', 'is_staff', 'date_joined']
    list_filter = ['skill_level', 'is_staff']
    search_fields = ['email', 'username']
