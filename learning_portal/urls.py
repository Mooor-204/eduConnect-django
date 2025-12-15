from django.urls import path
from . import views

app_name = 'learning_portal'

urlpatterns = [
    path('', views.learning_portal_home, name='home'),
    path('major/<str:major>/', views.courses_by_major, name='courses_by_major'),
]