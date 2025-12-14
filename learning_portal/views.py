from django.shortcuts import render
from .models import Course

def learning_portal_home(request):
    """Home page showing all majors"""
    majors = dict(Course.MAJOR_CHOICES)
    return render(request, 'learning_portal/home.html', {'majors': majors})

def courses_by_major(request, major):
    """Show courses for a specific major"""
    courses = Course.objects.filter(major=major)
    major_name = dict(Course.MAJOR_CHOICES).get(major, major)
    return render(request, 'learning_portal/courses.html', {
        'courses': courses,
        'major_name': major_name,
        'major_code': major
    })