from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from customauth.models import User

# Create your tests here.
class AuthTests(APITestCase):
    def setUp(self):
        self.login_url = reverse('login')
        self.signup_url = reverse('signup')
        
        data = {
            'email': 'testuser3@gmail.com',
            'first_name':'Test3',
            'last_name':'User'
        }
        self.testuser = User(**data)
        self.testuser.set_password("Hello@123")
        self.testuser.save()
        data = {
            'email': self.testuser.email,
            'password':'Hello@123'
        }    
        response = self.client.post(self.login_url,data)
        self.testusertoken = response.data.get('access_token')
        
        self.delete_user_url = reverse('delete-user',kwargs={'pk':self.testuser.id})
        self.delete_user_url2 = reverse('delete-user',kwargs={'pk':40})
        
        
        data = {
            'email': 'testuser4@gmail.com',
            'first_name':'Test4',
            'last_name':'User'
        }
        self.testuser2 = User(**data)
        self.testuser2.set_password("Hello@123")
        self.testuser2.save()
    
        data = {
            'email': self.testuser2.email,
            'password':'Hello@123'
        }    
        response = self.client.post(self.login_url,data)
        self.testuser2token = response.data.get('access_token')
        
        self.adminuser = User(
            first_name = 'Super',
            last_name = 'admin',
            email = 'superadmin@gmail.com',
            is_admin = True,
            is_staff = True
        )
        self.adminuser.set_password("Hello@123")
        self.adminuser.save()
        data = {
            'email': self.adminuser.email,
            'password':'Hello@123'
        }    
        response = self.client.post(self.login_url,data)
        self.adminusertoken = response.data.get('access_token')
        
        
     
    
    def test_signup_invalid_password2(self):
        # Test if user can successfully signup
        data = {
            'email': 'testuser@gmail.com',
            'password':'Hello@123',
            'first_name':'Test',
            'last_name':'User'
        }
        response = self.client.post(self.signup_url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)    
        
    def test_signup_invalid_email(self):
        # Test if user provided not a valid email
        data = {
            'email': 'testusergmail.com',
            'password':'Hello@123',
            'password2':'Hello@123',
            'first_name':'Test',
            'last_name':'User'
        }
        response = self.client.post(self.signup_url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
    
    def test_signup(self):
        # Test is user can successfully signup
        data = {
            'email': 'testuser@gmail.com',
            'password':'Hello@123',
            'password2':'Hello@123',
            'first_name':'Test',
            'last_name':'User'
        }
        response = self.client.post(self.signup_url,data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertGreaterEqual(User.objects.count() ,1)
        self.assertTrue(User.objects.filter(email=data['email']).exists())    
    
    def test_signup_invalid_existing_email(self):
        # Test if user can successfully signup
        self.test_signup()
        
        data = {
            'email': 'testuser@gmail.com',
            'password':'Hello@123',
            'first_name':'Test',
            'last_name':'User'
        }
        response = self.client.post(self.signup_url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST) 
    
    def test_login(self):
        # Test if user successfully sigin and recieve token
        
        self.test_signup()
        data = {
            'email': 'testuser@gmail.com',
            'password':'Hello@123'
        }    
        response = self.client.post(self.login_url,data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIn('access_token',response.data)
        self.assertIn('refresh_token',response.data)
    
    def test_login_fail(self):
        # Test if user provided invalid email and password
        data = {
            'email': 'testuser2@gmail.com',
            'password':'Hello@123'
        }
        response = self.client.post(self.login_url,data)
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_login_invalid_email(self):
        # Test if user provided invalid email and password

        data = {
            'password':'Hello@123'
        }
        response = self.client.post(self.login_url,data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
    def test_delete_user_by_user(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.testuser2token}')
        response = self.client.delete(self.delete_user_url)
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)  
    
    
    def test_delete_user_by_logeduser(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.testusertoken}')
        response = self.client.delete(self.delete_user_url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)    
    
    def test_delete_user_admin(self):
        # print(self.delete_user_url)
        # print(self.testuser)
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.adminusertoken}')
        response = self.client.delete(self.delete_user_url)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT) 
    
    
    def test_delete_user_no_match(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.adminusertoken}')
        response = self.client.delete(self.delete_user_url2)
        self.assertEqual(response.status_code,status.HTTP_404_NOT_FOUND)      
    