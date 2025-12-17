from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from universities.models import Faculty
from calculation.models import Application

class CalculationViewsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.client.login(username='testuser', password='password')
        self.faculty = Faculty.objects.create(
            name="Test Faculty",
            fees=10000
        )

    def test_calculator_home_view(self):
        url = reverse('calculation:calculator_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_thanawya_view(self):
        url = reverse('calculation:thanawya_calc')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_american_view(self):
        url = reverse('calculation:american_calc')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_igcse_view(self):
        url = reverse('calculation:igcse_calc')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_calculation_results_view(self):
        url = reverse('calculation:calculation_results', kwargs={'percentage': '85'})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_apply_to_faculty_view(self):
        url = reverse('calculation:apply_faculty', kwargs={'faculty_id': self.faculty.id})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Application.objects.filter(user=self.user, faculty=self.faculty).exists())

    def test_my_applications_view(self):
        url = reverse('calculation:my_applications')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
