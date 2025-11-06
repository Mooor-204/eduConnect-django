from django.db import models

from django.db import models
from django.contrib.auth.models import User

class Faculty(models.Model):
    EDUCATION_SYSTEMS = [
        ('american', 'American'),
        ('igcse', 'IGCSE'),
        ('national', 'National'),
    ]
    
    NATIONAL_CATEGORIES = [
        ('literature', 'Literature'),
        ('scientific_science', 'Scientific Science'),
        ('scientific_mathematics', 'Scientific Mathematics'),
    ]
    
    name = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    fees = models.IntegerField()
    credits = models.IntegerField()
    required_percent = models.FloatField()
    extra_requirements = models.TextField()
    education_system = models.CharField(max_length=20, choices=EDUCATION_SYSTEMS)
    national_category = models.CharField(max_length=25, choices=NATIONAL_CATEGORIES, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} - {self.university}"

class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    high_school_percent = models.FloatField(null=True, blank=True)
    education_system = models.CharField(max_length=20, choices=Faculty.EDUCATION_SYSTEMS)
    national_category = models.CharField(max_length=25, choices=Faculty.NATIONAL_CATEGORIES, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.high_school_percent}%"