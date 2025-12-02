from django.urls import path
from . import views

urlpatterns = [
    path('account/', views.account_view, name='account'),
    path('settings/', views.settings_view, name='settings'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('logout/', views.logout_view, name='logout'),
]