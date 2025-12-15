from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages

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

@login_required
def change_password_view(request):
    """
    View for users to change their password
    """
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'profile_menu/change_password.html', {
        'form': form
    })


@login_required
def notifications_view(request):
    """Let users choose what notifications they want"""
    
    
    defaults = {
        'app_updates': True,     
        'deadlines': True,      
        'newsletter': False,      
        'sms_alerts': False,      
    }
    

    if request.method == 'POST':
      
        app_updates = 'app_updates' in request.POST
        deadlines = 'deadlines' in request.POST  
        newsletter = 'newsletter' in request.POST
        sms_alerts = 'sms_alerts' in request.POST
        
        request.session['notify_app'] = app_updates
        request.session['notify_deadline'] = deadlines
        request.session['notify_news'] = newsletter
        request.session['notify_sms'] = sms_alerts
        
      
        messages.success(request, 'Your notification settings have been saved.')
        
        
        return redirect('notifications')
    
    context = {
        'app_updates': request.session.get('notify_app', defaults['app_updates']),
        'deadlines': request.session.get('notify_deadline', defaults['deadlines']),
        'newsletter': request.session.get('notify_news', defaults['newsletter']),
        'sms_alerts': request.session.get('notify_sms', defaults['sms_alerts']),
    }
    
    return render(request, 'profile_menu/notifications.html', context)
