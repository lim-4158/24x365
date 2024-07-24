from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

class UserAuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()  # Use APIClient for REST framework testing
        self.register_url = '/api/register/'  # Update with your actual register URL
        self.login_url = '/api/login/'  # Update with your actual login URL
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.token = self._get_token()

    def _get_token(self):
        """
        Helper function to get an authentication token for a user
        """
        token, created = Token.objects.get_or_create(user=self.user)
        return token.key

    def test_register_user(self):
        data = {
            'username': 'newuser',
            'password': 'newpassword'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response_data = response.json()
        self.assertIn('username', response_data)
        self.assertEqual(response_data['username'], 'newuser')


    def test_register_user_invalid_data(self):
        data = {
            'username': '',  # Invalid username
            'password': 'password'
        }
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.json())

    def test_login_user_success(self):
        data = {
            'username': self.username,
            'password': self.password
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.json())

    def test_login_user_invalid_credentials(self):
        data = {
            'username': self.username,
            'password': 'wrongpassword'  # Invalid password
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid Credentials')

    def test_login_user_nonexistent(self):
        data = {
            'username': 'nonexistentuser',
            'password': 'somepassword'
        }
        response = self.client.post(self.login_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn('error', response.json())
        self.assertEqual(response.json()['error'], 'Invalid Credentials')
