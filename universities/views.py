from django.shortcuts import render
from .models import Faculty

def universities_list(request):
    faculties = Faculty.objects.all()
    return render(request, 'universities/list.html', {'faculties': faculties})