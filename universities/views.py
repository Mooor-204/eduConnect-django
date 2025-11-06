from django.shortcuts import render

def universities_list(request):
    return render(request, 'universities/list.html')