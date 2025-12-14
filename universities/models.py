from django.db import models
from django.utils import timezone
from datetime import timedelta

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
    tests_assigned = models.BooleanField(default=False)
    math_test_url = models.URLField(blank=True)
    english_test_url = models.URLField(blank=True)
    test_deadline = models.DateField(null=True, blank=True)
    
    class Meta:
        unique_together = ['student', 'faculty']
    
    def __str__(self):
        return f"{self.student.username} → {self.faculty.name} ({self.status})"
    
    def save(self, *args, **kwargs):
        """Automatically assign tests when status changes to ACCEPTED"""
        
        if self.pk:  
            try:
                old_status = FacultyApplication.objects.get(pk=self.pk).status
                
                if old_status != 'ACCEPTED' and self.status == 'ACCEPTED':
                    self.assign_tests()
            except FacultyApplication.DoesNotExist:
                pass
        
        elif self.status == 'ACCEPTED':
            self.assign_tests()
        
        super().save(*args, **kwargs)
    
    def assign_tests(self):
        """Assign ACTUAL placement tests when application is approved"""
        self.tests_assigned = True
        
        self.math_test_url = "https://docs.google.com/forms/d/e/1FAIpQLSd4oeXOyEHDxeGRA6Pj2nMBHPQDyGazo1pChBy8CFkNBucPfA/viewform"
        
        self.english_test_url = "https://www.efset.org/quick-check/"
        
        self.test_deadline = timezone.now() + timedelta(days=14)