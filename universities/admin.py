from django.contrib import admin
from django.utils import timezone
from .models import Faculty, FacultyApplication

@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
    list_display = ['name', 'university', 'fees', 'required_percent', 'is_applications_open', 'application_deadline']
    list_filter = ['university', 'education_system', 'is_applications_open']
    search_fields = ['name', 'university']
    list_editable = ['is_applications_open']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'university', 'education_system')
        }),
        ('Academic Requirements', {
            'fields': ('required_percent', 'credits', 'extra_requirements')
        }),
        ('Financial Information', {
            'fields': ('fees',)
        }),
        ('Application Settings', {
            'fields': ('is_applications_open', 'application_deadline', 'application_form_url'),
            'classes': ('collapse',)
        }),
    )

@admin.register(FacultyApplication)
class FacultyApplicationAdmin(admin.ModelAdmin):
    list_display = ['student', 'faculty_name', 'university', 'status', 'tests_assigned', 'applied_at', 'decision_date']
    list_filter = ['status', 'faculty__university', 'applied_at', 'tests_assigned']
    search_fields = ['student__username', 'student__email', 'faculty__name']
    list_editable = ['status']
    readonly_fields = ['applied_at']
    actions = ['mark_accepted', 'mark_rejected', 'mark_under_review']  # Removed custom action
    
    fieldsets = (
        ('Application Details', {
            'fields': ('student', 'faculty', 'status', 'applied_at')
        }),
        ('Placement Tests', {
            'fields': ('tests_assigned', 'math_test_url', 'english_test_url', 'test_deadline'),
            'classes': ('collapse',)
        }),
        ('Review Process', {
            'fields': ('admin_notes', 'decision_date'),
            'classes': ('collapse',)
        }),
    )
    
    def faculty_name(self, obj):
        return obj.faculty.name
    faculty_name.short_description = 'Faculty Name'
    faculty_name.admin_order_field = 'faculty__name'
    
    def university(self, obj):
        return obj.faculty.university
    university.short_description = 'University'
    university.admin_order_field = 'faculty__university'
    
    @admin.action(description="✅ Mark as Accepted")
    def mark_accepted(self, request, queryset):
        """Just changes status - tests will be assigned automatically"""
        updated = queryset.update(status='ACCEPTED')
        self.message_user(request, f"{updated} application(s) marked as Accepted. Tests assigned automatically.")
    
    @admin.action(description="❌ Mark as Rejected")
    def mark_rejected(self, request, queryset):
        updated = queryset.update(status='REJECTED')
        self.message_user(request, f"{updated} application(s) marked as Rejected.")
    
    @admin.action(description="🔍 Mark as Under Review")
    def mark_under_review(self, request, queryset):
        updated = queryset.update(status='UNDER_REVIEW')
        self.message_user(request, f"{updated} application(s) marked as Under Review.")
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.order_by('-applied_at')