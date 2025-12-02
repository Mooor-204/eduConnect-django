from django.db import models
from django.contrib.auth.models import User

class UserAcademicRecord(models.Model):
    EDUCATION_TYPES = [
        ('thanawya', 'Thanawya Amma'),
        ('american', 'American Diploma'),
        ('igcse', 'IGCSE'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    education_type = models.CharField(max_length=20, choices=EDUCATION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Thanawya Amma fields
    thanawya_total_marks = models.FloatField(null=True, blank=True)
    
    # American Diploma fields
    american_gpa = models.FloatField(null=True, blank=True)
    american_sat1_score = models.IntegerField(null=True, blank=True)
    american_sat2_score = models.IntegerField(null=True, blank=True)
    
    # IGCSE fields
    igcse_subjects = models.JSONField(null=True, blank=True)  # Store as [{"subject": "Math", "grade": "A*"}, ...]
    
    # Calculated percentage
    final_percentage = models.FloatField(null=True, blank=True)

