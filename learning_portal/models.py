# learning_portal/models.py
from django.db import models

class Course(models.Model):
    MAJOR_CHOICES = [
        ('CS', 'Computer Science'),
        ('ENG', 'Engineering'),
        ('MED', 'Medicine'),
        ('BUS', 'Business'),
        ('ART', 'Arts & Humanities'),
    ]
    
    title = models.CharField(max_length=200)
    major = models.CharField(max_length=50, choices=MAJOR_CHOICES)
    provider = models.CharField(max_length=100)
    url = models.URLField()
    duration_hours = models.IntegerField()
    free = models.BooleanField(default=True)
    description = models.TextField()

    
    def __str__(self):
        return f"{self.title} ({self.get_major_display()})"