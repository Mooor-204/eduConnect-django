from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AuthAppTests(TestCase):
    def setUp(self):
        # Create a test user
        self.username = "testuser"
        self.password = "testpass123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.client = Client()

    def test_signup_view_get(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth_app/signup.html')

    def test_signup_view_post_success(self):
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'newpassword123',
            'password2': 'newpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to home
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_signup_view_post_failure(self):
        response = self.client.post(reverse('signup'), {
            'username': '',  # Missing username
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'This field is required')

    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth_app/login.html')

    def test_login_view_post_success(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)  # Redirects to home
        self.assertTrue('_auth_user_id' in self.client.session)

    def test_login_view_post_failure(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Invalid username or password.')

    def test_logout_view(self):
        # First log in
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirects to home
        self.assertFalse('_auth_user_id' in self.client.session)
