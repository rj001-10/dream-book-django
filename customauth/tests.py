from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from customauth.models import User

# Create your tests here.
class AuthTests(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        
    
    def test_signup_invalid_password2(self):
        # Test if user can successfully signup
        data = {
            'email': 'testuser@gmail.com',
            'password':'Golden_123',
            'first_name':'Test',
            'last_name':'User'
        }
        response = self.client.post(self.signup_url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)    
        
    def test_signup_invalid_email(self):
        # Test if user provided not a valid email
        data = {
            'email': 'testusergmail.com',
            'password':'Golden_123',
            'password2':'Golden_123',
            'first_name':'Test',
            'last_name':'User'
        }
        response = self.client.post(self.signup_url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_signup(self):
        # Test is user can successfully signup
        data = {
            'email': 'testuser@gmail.com',
            'password':'Golden_123',
            'password2':'Golden_123',
            'first_name':'Test',
            'last_name':'User'
        }
        response = self.client.post(self.signup_url,data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(),1)
        self.assertEqual(User.objects.get().email,data['email'])    
    
    def test_login(self):
        # Test if user successfully sigin and recieve token
        
        self.test_signup()
        data = {
            'email': 'testuser@gmail.com',
            'password':'Golden_123'
        }    
        response = self.client.post(self.login_url,data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('access_token',response.data)
        self.assertIn('refresh_token',response.data)
    
    def test_login_fail(self):
        # Test if user provided invalid email and password
        data = {
            'email': 'testuser2@gmail.com',
            'password':'Golden_123'
        }
        response = self.client.post(self.login_url,data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_login_invalid_email(self):
        # Test if user provided invalid email and password

        data = {
            'password':'Golden_123'
        }
        response = self.client.post(self.login_url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    