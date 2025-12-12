from django.urls import path
from . import views

app_name = 'calculation'

urlpatterns = [
    path('', views.calculation_calculator, name='calculator_home'),
    path('thanawya/', views.thanawya_calculator, name='thanawya_calc'),
    path('american/', views.american_calculator, name='american_calc'),
    path('igcse/', views.igcse_calculator, name='igcse_calc'),
    path('results/<str:percentage>/', views.calculation_results, name='calculation_results'),
    path('apply/<int:faculty_id>/', views.apply_to_faculty, name='apply_faculty'),
]