from django.db import models

class Faculty(models.Model):
    EDUCATION_SYSTEMS = [
        ('american', 'American'),
        ('igcse', 'IGCSE'),
        ('national', 'National'),
    ]
    
    name = models.CharField(max_length=200)
    university = models.CharField(max_length=200)
    fees = models.IntegerField()
    credits = models.IntegerField(default=120)
    required_percent = models.FloatField()
    extra_requirements = models.TextField()
    education_system = models.CharField(max_length=20, choices=EDUCATION_SYSTEMS, default='national')
    
    def __str__(self):
        return f"{self.name} - {self.university}"