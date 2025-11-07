from django import forms
from .models import UserAcademicRecord

class ThanawyaForm(forms.Form):
    total_marks = forms.FloatField(
        label='Total Marks (out of 410)',
        min_value=0,
        max_value=410,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )

class AmericanForm(forms.Form):
    gpa = forms.FloatField(
        label='GPA (out of 4.0)',
        min_value=0,
        max_value=4.0,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'})
    )
    sat1_score = forms.IntegerField(
        label='SAT I Score (out of 1600)',
        min_value=400,
        max_value=1600,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    sat2_score = forms.IntegerField(
        label='SAT II Score (out of 1600)',
        min_value=400,
        max_value=1600,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
class IGCSEForm(forms.Form):
    subjects = forms.CharField(
        label='Enter your subjects and grades (format: Subject:Grade, one per line)',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 8,
            'placeholder': 'Math: A*\nPhysics: A\nChemistry: B\nBiology: A\nEnglish: A*\nArabic: B\nHistory: C\nGeography: B'
        }),
        help_text='Enter each subject and grade in format "Subject: Grade". Grades: A*, A, B, C, D, E'
    )