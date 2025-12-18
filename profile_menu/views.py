from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from datetime import datetime
import calendar

@login_required
def account_view(request):
    return render(request, 'profile_menu/account.html', {'user': request.user})

@login_required
def settings_view(request):
    context = {
        'profile_visible': request.session.get('profile_visible', True),
    }
    return render(request, 'profile_menu/settings.html', context)

def logout_view(request):
    auth_logout(request)
    return redirect('login')

@login_required
def change_password_view(request):
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
    return render(request, 'profile_menu/change_password.html', {'form': form})

@login_required
def notifications_view(request):
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

@login_required
def privacy_settings_view(request):
    if request.method == 'POST':
        profile_visible = 'profile_visible' in request.POST
        request.session['profile_visible'] = profile_visible
        messages.success(request, 'Privacy settings updated!')
        return redirect('settings')
    return render(request, 'profile_menu/privacy_settings.html')

@login_required
def calendar_view(request):
    today = datetime.now()
    
    year = int(request.GET.get('year', today.year))
    month = int(request.GET.get('month', today.month))
    
    prev_month = month - 1
    prev_year = year
    if prev_month == 0:
        prev_month = 12
        prev_year = year - 1
    
    next_month = month + 1
    next_year = year
    if next_month == 13:
        next_month = 1
        next_year = year + 1
    
    deadlines_by_day = {}
    
    try:
        from universities.models import FacultyApplication
        user_applications = FacultyApplication.objects.filter(student=request.user)
        
        for app in user_applications:
            if app.faculty.application_deadline:
                deadline_date = app.faculty.application_deadline
                if deadline_date.year == year and deadline_date.month == month:
                    day = deadline_date.day
                    if day not in deadlines_by_day:
                        deadlines_by_day[day] = []
                    deadlines_by_day[day].append({
                        'title': f'App Deadline: {app.faculty.university}',
                        'type': 'application',
                        'color': '#dc3545',
                        'icon': '📝',
                        'university': app.faculty.university,
                    })
            
            if app.status == 'ACCEPTED' and app.test_deadline:
                test_date = app.test_deadline
                if test_date.year == year and test_date.month == month:
                    day = test_date.day
                    if day not in deadlines_by_day:
                        deadlines_by_day[day] = []
                    deadlines_by_day[day].append({
                        'title': f'Placement Test: {app.faculty.university}',
                        'type': 'test',
                        'color': '#007bff',
                        'icon': '📚',
                        'university': app.faculty.university,
                        'math_url': app.math_test_url,
                        'english_url': app.english_test_url,
                    })
            
            if app.test_completion_date:
                completion_date = app.test_completion_date
                if completion_date.year == year and completion_date.month == month:
                    day = completion_date.day
                    if day not in deadlines_by_day:
                        deadlines_by_day[day] = []
                    deadlines_by_day[day].append({
                        'title': f'Test Submitted: {app.faculty.university}',
                        'type': 'submission',
                        'color': '#28a745',
                        'icon': '✅',
                        'university': app.faculty.university,
                    })
    except Exception as e:
        print(f"Calendar error: {e}")
        pass
    
    cal = calendar.monthcalendar(year, month)
    
    context = {
        'year': year,
        'month': month,
        'month_name': calendar.month_name[month],
        'calendar': cal,
        'today': today.day if today.year == year and today.month == month else None,
        'deadlines_by_day': deadlines_by_day,
        'prev_month': prev_month,
        'prev_year': prev_year,
        'next_month': next_month,
        'next_year': next_year,
    }
    return render(request, 'profile_menu/calendar.html', context)