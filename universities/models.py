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
    
    # ✅ ADD THESE 3 FIELDS (PROPERLY INDENTED):
    application_form_url = models.URLField(max_length=500, blank=True, null=True)
    application_deadline = models.DateField(blank=True, null=True)
    is_applications_open = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.university}"


class FacultyApplication(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Review'),
        ('SUBMITTED', 'Form Submitted'),
        ('UNDER_REVIEW', 'Under Review'),
        ('ACCEPTED', 'Accepted'),
        ('REJECTED', 'Rejected'),
    ]
    
    student = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE)
    applied_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    admin_notes = models.TextField(blank=True)
    decision_date = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        unique_together = ['student', 'faculty']
    
    def __str__(self):
        return f"{self.student.username} → {self.faculty.name} ({self.status})"