from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import UserAcademicRecord
from .forms import ThanawyaForm, AmericanForm, IGCSEForm
from universities.models import Faculty, FacultyApplication
from .recommender import recommend_faculties_for_user


GRADE_PERCENTAGE = {
    'A*': 100,
    'A': 95,
    'B': 85,
    'C': 75,
    'D': 65,
    'E': 55
}

@login_required
def calculation_calculator(request):
    return render(request, 'calculation/calculator_home.html')

@login_required
def thanawya_calculator(request):
    if request.method == 'POST':
        form = ThanawyaForm(request.POST)
        if form.is_valid():
            total_marks = form.cleaned_data['total_marks']
            percentage = (total_marks / 410) * 100
            
            
            record = UserAcademicRecord(
                user=request.user,
                education_type='thanawya',
                thanawya_total_marks=total_marks,
                final_percentage=percentage
            )
            record.save()
            
            return redirect('calculation:calculation_results', percentage=str(percentage))
    else:
        form = ThanawyaForm()
    
    return render(request, 'calculation/thanawya_form.html', {'form': form})

@login_required
def american_calculator(request):
    if request.method == 'POST':
        form = AmericanForm(request.POST)
        if form.is_valid():
            gpa = form.cleaned_data['gpa']
            sat1_score = form.cleaned_data['sat1_score']
            sat2_score = form.cleaned_data['sat2_score'] or 0
            
            print(f"DEBUG - GPA: {gpa}, SAT I: {sat1_score}, SAT II: {sat2_score}")
            
            
            gpa_percentage = gpa * 25
            print(f"DEBUG - GPA Percentage: {gpa_percentage}")
            
            
            sat1_percentage = (sat1_score / 1600) * 100
            print(f"DEBUG - SAT I Percentage: {sat1_percentage}")
            
            
            sat2_percentage = (sat2_score / 1600) * 100 if sat2_score > 0 else 0
            print(f"DEBUG - SAT II Percentage: {sat2_percentage}")
            
            
            if sat2_score > 0:
                
                final_percentage = (gpa_percentage * 0.4) + (sat1_percentage * 0.3) + (sat2_percentage * 0.3)
                print(f"DEBUG - Using 40-30-30 weights")
            else:
                 
                final_percentage = (gpa_percentage * 0.4) + (sat1_percentage * 0.6)
                print(f"DEBUG - Using 40-60-0 weights")
            
            print(f"DEBUG - Final Percentage: {final_percentage}")
            
            
            record = UserAcademicRecord(
                user=request.user,
                education_type='american',
                american_gpa=gpa,
                american_sat1_score=sat1_score,
                american_sat2_score=sat2_score,
                final_percentage=final_percentage
            )
            record.save()
            
            return redirect('calculation:calculation_results', percentage=str(final_percentage))
    else:
        form = AmericanForm()
    
    return render(request, 'calculation/american_form.html', {'form': form})

@login_required
def igcse_calculator(request):
    if request.method == 'POST':
        form = IGCSEForm(request.POST)
        if form.is_valid():
            subjects_text = form.cleaned_data['subjects']
            subjects_list = []
            total_percentage = 0
            subject_count = 0
            
            
            for line in subjects_text.split('\n'):
                line = line.strip()
                if ':' in line:
                    subject, grade = line.split(':', 1)
                    subject = subject.strip()
                    grade = grade.strip().upper()
                    
                    if grade in GRADE_PERCENTAGE:
                        subjects_list.append({
                            'subject': subject,
                            'grade': grade
                        })
                        total_percentage += GRADE_PERCENTAGE[grade]
                        subject_count += 1
            
            if subject_count > 0:
                final_percentage = total_percentage / subject_count
            else:
                final_percentage = 0
            
           
            record = UserAcademicRecord(
                user=request.user,
                education_type='igcse',
                igcse_subjects=subjects_list,
                final_percentage=final_percentage
            )
            record.save()
            
            return redirect('calculation:calculation_results', percentage=str(final_percentage))
    else:
        form = IGCSEForm()
    
    return render(request, 'calculation/igcse_form.html', {'form': form})

@login_required
def calculation_results(request, percentage):
    try:
        
        percentage_float = float(percentage)
    except (ValueError, TypeError):
        percentage_float = 0.0
    
    
    eligible_faculties = Faculty.objects.filter(required_percent__lte=percentage_float)
    
    
    applied_faculty_ids = []
    if request.user.is_authenticated:
        applied_faculty_ids = FacultyApplication.objects.filter(
            student=request.user
        ).values_list('faculty_id', flat=True)
    
    context = {
        'percentage': round(percentage_float, 2),
        'eligible_faculties': eligible_faculties,
        'applied_faculty_ids': list(applied_faculty_ids),  # Convert to list for template
    }
    return render(request, 'calculation/results.html', context)

def results_view(request):
    # ... your existing calculation code ...
    
    # Get the user's latest academic record
    from .models import UserAcademicRecord
    try:
        user_record = UserAcademicRecord.objects.filter(
            user=request.user
        ).latest('created_at')
    except UserAcademicRecord.DoesNotExist:
        user_record = None
    
    # Get recommendations if record exists
    recommendations = []
    if user_record and user_record.final_percentage:
        recommendations = recommend_faculties_for_user(user_record)
    
    context = {
        'user_record': user_record,
        'recommendations': recommendations,
    }
    
    return render(request, 'calculation/results.html', context)

# ✅ NEW FUNCTION ADDED HERE:
@login_required
def apply_to_faculty(request, faculty_id):
    """
    Handle Apply Now button click:
    1. Record application in database
    2. Redirect to Google Form
    """
    # Get the faculty
    faculty = get_object_or_404(Faculty, id=faculty_id)
    student = request.user
    
    # Check if applications are open
    if not faculty.is_applications_open:
        messages.error(request, f"Applications for {faculty.name} are currently closed.")
        return redirect('calculation:calculation_results', percentage=request.GET.get('percentage', '0'))
    
    # Check if already applied
    if FacultyApplication.objects.filter(student=student, faculty=faculty).exists():
        messages.warning(request, f"You have already applied to {faculty.name}!")
    else:
        # Create application record
        FacultyApplication.objects.create(
            student=student, 
            faculty=faculty,
            status='SUBMITTED'
        )
        messages.success(request, f"Application submitted for {faculty.name}!")
    
    # Redirect to Google Form
    if faculty.application_form_url:
        return redirect(faculty.application_form_url)
    else:
        messages.error(request, "Application form link not available. Please contact the university.")
        return redirect('calculation:calculation_results', percentage=request.GET.get('percentage', '0'))