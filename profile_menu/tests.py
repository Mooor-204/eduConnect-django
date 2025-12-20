from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()

class ChangePasswordTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='old_password123'
        )
        self.client.login(username='testuser', password='old_password123')

    def test_password_change_page_accessible(self):
        url = reverse('change_password')  
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<form')  

    def test_password_change_success(self):
        url = reverse('change_password')  
        response = self.client.post(url, {
            'old_password': 'old_password123',
            'new_password1': 'NewStrongPass123',
            'new_password2': 'NewStrongPass123'
        }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Your password was successfully updated!')

        
        self.client.logout()
        login = self.client.login(username='testuser', password='NewStrongPass123')
        self.assertTrue(login)

    def test_password_change_invalid(self):
        url = reverse('change_password')  
        response = self.client.post(url, {
            'old_password': 'wrong_old_password',
            'new_password1': 'NewStrongPass123',
            'new_password2': 'NewStrongPass123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Please correct the errors below.')