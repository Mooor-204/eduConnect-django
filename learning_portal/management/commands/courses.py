from django.core.management.base import BaseCommand
from learning_portal.models import Course

class Command(BaseCommand):
    help = 'Seed sample courses for learning portal'
    
    def handle(self, *args, **kwargs):
        courses_data = [
            # Computer Science Courses
            {
                'title': 'CS50: Introduction to Computer Science - Harvard',
                'major': 'CS',
                'provider': 'edX',
                'url': 'https://www.edx.org/cs50',
                'duration_hours': 100,
                'free': True,
                'description': 'Harvard\'s famous introduction to computer science and programming'
            },
            {
                'title': 'Python for Everybody - University of Michigan',
                'major': 'CS',
                'provider': 'Coursera',
                'url': 'https://www.coursera.org/specializations/python',
                'duration_hours': 80,
                'free': True,
                'description': 'Learn Python programming from basics to advanced concepts'
            },
            {
                'title': 'Web Development Bootcamp',
                'major': 'CS',
                'provider': 'Udemy',
                'url': 'https://www.udemy.com/course/the-web-developer-bootcamp/',
                'duration_hours': 60,
                'free': False,
                'description': 'Full-stack web development with HTML, CSS, JavaScript, Node.js'
            },
            
            # Engineering Courses
            {
                'title': 'Engineering Mechanics: Statics',
                'major': 'ENG',
                'provider': 'Khan Academy',
                'url': 'https://www.khanacademy.org/science/physics',
                'duration_hours': 40,
                'free': True,
                'description': 'Fundamental concepts of forces and equilibrium'
            },
            {
                'title': 'Introduction to Electrical Engineering',
                'major': 'ENG',
                'provider': 'MIT OpenCourseWare',
                'url': 'https://ocw.mit.edu/courses/electrical-engineering',
                'duration_hours': 50,
                'free': True,
                'description': 'Basic electrical engineering concepts and circuits'
            },
            
            # Medicine Courses
            {
                'title': 'Human Anatomy & Physiology',
                'major': 'MED',
                'provider': 'Coursera',
                'url': 'https://www.coursera.org/learn/anatomy',
                'duration_hours': 70,
                'free': True,
                'description': 'Comprehensive introduction to human body systems'
            },
            {
                'title': 'Medical Terminology',
                'major': 'MED',
                'provider': 'edX',
                'url': 'https://www.edx.org/learn/medical-terminology',
                'duration_hours': 30,
                'free': True,
                'description': 'Learn the language of healthcare professionals'
            },
            
            # Business Courses
            {
                'title': 'Introduction to Finance',
                'major': 'BUS',
                'provider': 'Coursera',
                'url': 'https://www.coursera.org/learn/introduction-to-finance',
                'duration_hours': 45,
                'free': True,
                'description': 'Fundamental concepts of corporate finance and accounting'
            },
            {
                'title': 'Marketing Fundamentals',
                'major': 'BUS',
                'provider': 'edX',
                'url': 'https://www.edx.org/learn/marketing',
                'duration_hours': 35,
                'free': True,
                'description': 'Basic principles of marketing and consumer behavior'
            },
            
            # Arts & Humanities
            {
                'title': 'Introduction to Philosophy',
                'major': 'ART',
                'provider': 'Coursera',
                'url': 'https://www.coursera.org/learn/philosophy',
                'duration_hours': 25,
                'free': True,
                'description': 'Explore fundamental philosophical questions and thinkers'
            },
            
            # Natural Sciences
            {
                'title': 'General Chemistry',
                'major': 'SCI',
                'provider': 'Khan Academy',
                'url': 'https://www.khanacademy.org/science/chemistry',
                'duration_hours': 60,
                'free': True,
                'description': 'Comprehensive chemistry course for science students'
            }
        ]
        
        # Clear existing data (optional)
        Course.objects.all().delete()
        
        # Create courses
        created_count = 0
        for course_data in courses_data:
            course, created = Course.objects.get_or_create(
                title=course_data['title'],
                defaults=course_data
            )
            if created:
                created_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully seeded {created_count} courses')
        )