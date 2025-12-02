from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout

@login_required
def account_view(request):
    return render(request, 'profile_menu/account.html', {'user': request.user})

@login_required
def settings_view(request):
    return render(request, 'profile_menu/settings.html')

@login_required
def calendar_view(request):
    return render(request, 'profile_menu/calendar.html')

def logout_view(request):
    auth_logout(request)
    return redirect('login')