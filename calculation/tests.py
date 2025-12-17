from django.test import TestCase
from django.test import TestCase
from django.urls import reverse

class CalculationViewsTest(TestCase):

    def test_calculator_home_view(self):
        response = self.client.get(reverse('calculation:calculator_home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculation/calculator_home.html')

    def test_thanawya_view(self):
        response = self.client.get(reverse('calculation:thanawya_calc'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculation/thanawya_form.html')

    def test_american_view(self):
        response = self.client.get(reverse('calculation:american_calc'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculation/american_form.html')

    def test_igcse_view(self):
        response = self.client.get(reverse('calculation:igcse_calc'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculation/igcse_form.html')

    def test_calculation_results_view(self):
        percentage = "85"
        response = self.client.get(reverse('calculation:calculation_results', args=[percentage]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calculation/results.html')

    def test_apply_to_faculty_view(self):
       
        from universities.models import Faculty
        faculty = Faculty.objects.create(name="Test Faculty")
        response = self.client.get(reverse('calculation:apply_faculty', args=[faculty.id]))
        self.assertEqual(response.status_code, 302) 

    def test_my_applications_view(self):
        response = self.client.get(reverse('calculation:my_applications'))
        self.assertEqual(response.status_code, 302)  

