from django.contrib import admin
from .models import Course

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'major', 'provider', 'free', 'duration_hours')
    list_filter = ('major', 'provider', 'free')
    search_fields = ('title', 'description')
    list_per_page = 20