from django.contrib import admin
from .models import Subject, SyllabusTopic

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'created_at']
    search_fields = ['name', 'owner__email']
