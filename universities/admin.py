from django.contrib import admin
from .models import Faculty

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'fees', 'required_percent']
    list_filter = ['university', 'education_system']