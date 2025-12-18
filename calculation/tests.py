from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from calculation.models import UserAcademicRecord

User = get_user_model()

class UserAndCalculationTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            email="testuser@example.com",
            password="password123"
        )
        self.client = Client()

    def test_login_page_accessible(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_success(self):
        login = self.client.login(username="testuser", password="password123")
        self.assertTrue(login)

    def test_login_fail(self):
        login = self.client.login(username="testuser", password="wrongpassword")
        self.assertFalse(login)

    def test_american_calculation_cases(self):
        test_cases = [
            (4.0, 1600, None, 100.0, 100.0, 0.0, 70.0),
            (3.6, 1500, 1550, 90.0, 93.75, 96.875, 93.59375),
            (3.8, None, None, 95.0, 0.0, 0.0, 95.0),
        ]
        for gpa, sat_i, sat_ii, exp_gpa, exp_sat_i, exp_sat_ii, exp_final in test_cases:
            record = UserAcademicRecord.objects.create(
                user=self.user,
                gpa=gpa,
                sat_i=sat_i,
                sat_ii=sat_ii
            )
            latest = UserAcademicRecord.objects.latest('id')
            gpa_pct = (latest.gpa / 4.0) * 100
            sat_i_pct = (latest.sat_i / 1600 * 100) if latest.sat_i else 0
            sat_ii_pct = (latest.sat_ii / 1600 * 100) if latest.sat_ii else 0
            final = gpa_pct * 0.4 + sat_i_pct * 0.3 + sat_ii_pct * 0.3
            self.assertAlmostEqual(gpa_pct, exp_gpa)
            self.assertAlmostEqual(sat_i_pct, exp_sat_i)
            self.assertAlmostEqual(sat_ii_pct, exp_sat_ii)
            self.assertAlmostEqual(final, exp_final)

    def test_thanawya_calculation_cases(self):
        test_cases = [
            (95, 95.0),
            (88, 88.0),
            (100, 100.0),
        ]
        for grade, exp_pct in test_cases:
            record = UserAcademicRecord.objects.create(
                user=self.user,
                thanawya_score=grade
            )
            latest = UserAcademicRecord.objects.latest('id')
            self.assertEqual(latest.thanawya_score, grade)
            self.assertEqual(float(latest.thanawya_score), exp_pct)

    def test_igcse_calculation_cases(self):
        test_cases = [
            (4.0, 100.0),
            (3.5, 87.5),
            (3.8, 95.0),
        ]
        for gpa, exp_pct in test_cases:
            record = UserAcademicRecord.objects.create(
                user=self.user,
                igcse_gpa=gpa
            )
            latest = UserAcademicRecord.objects.latest('id')
            igcse_pct = (latest.igcse_gpa / 4.0) * 100
            self.assertAlmostEqual(igcse_pct, exp_pct)
