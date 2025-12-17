from django.test import TestCase
# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

class AuthAppTests(TestCase):
    
    def setUp(self):
        # Create a user for login tests
        self.user = User.objects.create_user(username='testuser', password='12345')

    def test_signup_view_get(self):
        # Test GET request returns status 200
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth_app/signup.html')

    def test_signup_view_post_success(self):
        # Test POST request creates a new user
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'Testpass123!',
            'password2': 'Testpass123!'
        })
        self.assertEqual(response.status_code, 302)  # redirect after signup
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_view_post_invalid(self):
        # Test POST with mismatched passwords
        response = self.client.post(reverse('signup'), {
            'username': 'failuser',
            'password1': 'abc',
            'password2': 'xyz'
        })
        self.assertEqual(response.status_code, 200)  # form reloads
        self.assertFalse(User.objects.filter(username='failuser').exists())

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth_app/login.html')

    def test_login_view_post_success(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': '12345'
        })
        self.assertEqual(response.status_code, 302)  # redirect after login
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)  # form reloads
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_logout_view(self):
        # First login
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # redirect after logout
        self.assertFalse('_auth_user_id' in self.client.session)

