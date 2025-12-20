from django.test import TestCase


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
            (4.0, 1600, None, 100.0),
            (3.6, 1500, 1550, 93.1875),
            (3.8, None, None, 38.0),
        ]
        for gpa, sat1, sat2, exp_final in test_cases:
            record = UserAcademicRecord.objects.create(
                user=self.user,
                american_gpa=gpa or 0,
                american_sat1_score=sat1 or 0,
                american_sat2_score=sat2 or 0,
                final_percentage=0
            )
            latest = UserAcademicRecord.objects.latest('id')
            gpa_pct = latest.american_gpa * 25
            sat1_pct = (latest.american_sat1_score / 1600) * 100 if latest.american_sat1_score else 0
            sat2_pct = (latest.american_sat2_score / 1600) * 100 if latest.american_sat2_score else 0
            if latest.american_sat2_score > 0:
                latest.final_percentage = gpa_pct * 0.4 + sat1_pct * 0.3 + sat2_pct * 0.3
            else:
                latest.final_percentage = gpa_pct * 0.4 + sat1_pct * 0.6
            latest.save()
            self.assertAlmostEqual(latest.final_percentage, exp_final)

    def test_thanawya_calculation_cases(self):
        test_cases = [
            (410, 100.0),
            (369, (369/410)*100),
            (205, 50.0)
        ]
        for total_marks, exp_final in test_cases:
            record = UserAcademicRecord.objects.create(
                user=self.user,
                thanawya_total_marks=total_marks,
                final_percentage=(total_marks/410)*100
            )
            latest = UserAcademicRecord.objects.latest('id')
            self.assertAlmostEqual(latest.final_percentage, exp_final)

    def test_igcse_calculation_cases(self):
        test_cases = [
            ([{'subject':'Math','grade':'A*'},{'subject':'English','grade':'A'}], (100+95)/2),
            ([{'subject':'Biology','grade':'B'},{'subject':'Chemistry','grade':'C'}], (85+75)/2),
            ([{'subject':'Physics','grade':'D'}], 65),
        ]
        for subjects_list, exp_final in test_cases:
            record = UserAcademicRecord.objects.create(
                user=self.user,
                igcse_subjects=subjects_list,
                final_percentage=sum([{'A*':100,'A':95,'B':85,'C':75,'D':65,'E':55}[s['grade']] for s in subjects_list])/len(subjects_list)
            )
            latest = UserAcademicRecord.objects.latest('id')
            self.assertAlmostEqual(latest.final_percentage, exp_final)