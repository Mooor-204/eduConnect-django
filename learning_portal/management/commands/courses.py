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
                'free': False,
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
                'title': 'Introduction to Electronics',
                'major': 'ENG',
                'provider': 'Coursera',
                'url': 'https://www.coursera.org/learn/electronics',
                'duration_hours': 45,
                'free': False,
                'description': 'Basic electronics and circuit design for beginners'
            },
            
            # Medicine Courses
            {
                'title': 'Health and Medicine - Khan Academy',
                'major': 'MED',
                'provider': 'Khan Academy',
                'url': 'https://www.khanacademy.org/science/health-and-medicine',
                'duration_hours': 80,
                'free': True,
                'description': 'Complete medical basics: anatomy, physiology, diseases, and healthcare'
               
            },
            {
                'title': 'Medical Neuroscience - Duke University',
                'major': 'MED',
                'provider': 'Coursera',
                'url': 'https://www.coursera.org/learn/medical-neuroscience',
                'duration_hours': 55,
                'free': False,
                'description': 'Comprehensive introduction to human nervous system'
                
            },
            {
                'title': 'Introduction to Human Physiology',
                'major': 'MED',
                'provider': 'Coursera',
                'url': 'https://www.coursera.org/learn/physiology',
                'duration_hours': 35,
                'free': False,
                'description': 'Fundamental concepts of human body function'
            },

            # Business Courses
            {
                'title': 'Financial Markets - Yale University',
                'major': 'BUS',
                'provider': 'Coursera',
                'url': 'https://www.coursera.org/learn/financial-markets-global',
                'duration_hours': 40,
                'free': False,
                'description': 'Nobel-winning professor Robert Shiller teaches financial markets, risk management, and behavioral finance'
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
                'free': False,
                'description': 'Explore fundamental philosophical questions and thinkers'
            },
            {
                'title': 'Moral Foundations of Politics - Yale',
                'major': 'ART',
                'provider': 'Coursera',
                'url': 'https://www.coursera.org/learn/moral-politics',
                'duration_hours': 40,
                'free': False,
                'description': 'Political philosophy exploring democracy, justice, and political legitimacy'
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
    
   