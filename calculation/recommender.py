
from universities.models import Faculty as UniversityFaculty

def recommend_faculties_for_user(user_academic_record):
    """
    Recommend university faculties based on user's academic record
    """
    # Get user's final percentage
    user_percentage = user_academic_record.final_percentage
    
    if not user_percentage:
        return []
    
    # Map calculation education type to university education system
    education_type_map = {
        'thanawya': 'national',
        'american': 'american',
        'igcse': 'igcse'
    }
    
    user_edu_system = education_type_map.get(
        user_academic_record.education_type, 
        'national'
    )
    
    # Find matching faculties
    matching_faculties = UniversityFaculty.objects.filter(
        required_percent__lte=user_percentage,
        education_system=user_edu_system
    ).order_by('required_percent', 'fees')
    
    return list(matching_faculties)  # Convert to list