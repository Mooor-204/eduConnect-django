from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from calculation.models import UserAcademicRecord


class CalculationAccuracyTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='calcuser',
            password='password123'
        )
        self.client.login(username='calcuser', password='password123')

    def test_thanawya_percentage_calculation(self):
        """
        410 total marks = 100%
        205 marks = 50%
        """
        self.client.post(
            reverse('calculation:thanawya_calc'),
            {'total_marks': 205}
        )

        record = UserAcademicRecord.objects.latest('id')
        expected_percentage = (205 / 410) * 100

        self.assertAlmostEqual(
            record.final_percentage,
            expected_percentage,
            places=2
        )

    def test_american_calculation_without_sat2(self):
        """
        GPA = 4.0 → 100%
        SAT I = 1600 → 100%
        Formula: (GPA% × 0.4) + (SAT I% × 0.6)
        Expected = 100%
        """
        self.client.post(
            reverse('calculation:american_calc'),
            {
                'gpa': 4.0,
                'sat1_score': 1600,
                'sat2_score': 0
            }
        )

        record = UserAcademicRecord.objects.latest('id')
        expected_percentage = (100 * 0.4) + (100 * 0.6)

        self.assertAlmostEqual(
            record.final_percentage,
            expected_percentage,
            places=2
        )

    def test_american_calculation_with_sat2(self):
        """
        GPA = 4.0 → 100%
        SAT I = 1600 → 100%
        SAT II = 1600 → 100%
        Formula: 40% + 30% + 30%
        """
        self.client.post(
            reverse('calculation:american_calc'),
            {
                'gpa': 4.0,
                'sat1_score': 1600,
                'sat2_score': 1600
            }
        )

        record = UserAcademicRecord.objects.latest('id')
        expected_percentage = (100 * 0.4) + (100 * 0.3) + (100 * 0.3)

        self.assertAlmostEqual(
            record.final_percentage,
            expected_percentage,
            places=2
        )

    def test_igcse_average_calculation(self):
        """
        A = 95
        B = 85
        C = 75
        Average = (95 + 85 + 75) / 3 = 85
        """
        self.client.post(
            reverse('calculation:igcse_calc'),
            {
                'subjects': 'Math:A\nPhysics:B\nChemistry:C'
            }
        )

        record = UserAcademicRecord.objects.latest('id')
        expected_percentage = (95 + 85 + 75) / 3

        self.assertAlmostEqual(
            record.final_percentage,
            expected_percentage,
            places=2
        )
