from rest_framework.test import APITestCase
from django.urls import reverse
from customauth.models import User
import os
from rest_framework import status
from dream.models import Dream
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.
class DreamCreateTests(APITestCase):
    def setUp(self):
        self.dream_list_url = reverse('dream-list')
        self.loginurl = reverse('login')
        
        # existing user create and login
        self.existing_user = User(
            first_name = 'Existing',
            last_name = 'User',
            email = 'existinguser@gmail.com',
        )
        self.existing_user.set_password("Hello@123")
        self.existing_user.save()
        data = {
            'email': self.existing_user.email,
            'password':'Hello@123'
        }    
        
        response = self.client.post(self.loginurl,data)
        self.existingusertoken = response.data.get('access_token')
        
        
        # setting up sample images
        self.image_path = os.path.join( 'media','dream_image', 'testdreamimg.jpg')
        self.invalid_img_path = os.path.join('media','dream_image', 'invalidimg.txt')
        
    def test_createDream_Invalid_auth(self):
        with open(self.image_path,'rb') as img_file:
            img = SimpleUploadedFile(name='testdreamimg.jpg', content=img_file.read(), content_type='image/jpeg')
            data = {
                'title': 'My first dream',
                'description':'It was horror dream there is so many monsters',
                'image':img,
                'is_public':False,
            } 
            
        
            response = self.client.post(self.dream_list_url,data,format='multipart')
            self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
    
    def test_createDream_title_required(self):
        with open(self.image_path,'rb') as img_file:
            img = SimpleUploadedFile(name='testdreamimg.jpg', content=img_file.read(), content_type='image/jpeg')
            data = {
                'description':'It was horror dream there is so many monsters',
                'image':img,
                'is_public':False,
            } 
            self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.existingusertoken}')
            
            response = self.client.post(self.dream_list_url,data,format='multipart')   
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_createDream_description_required(self):
        with open(self.image_path,'rb') as img_file:
            img = SimpleUploadedFile(name='testdreamimg.jpg', content=img_file.read(), content_type='image/jpeg')
            data = {
                'title': 'My first dream',
                'image':img,
            } 
            self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.existingusertoken}')
            
            response = self.client.post(self.dream_list_url,data,format='multipart')   
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)   
    
    def test_createDream_image_invalid(self):
        with open(self.invalid_img_path,'rb') as img_file:
            img = SimpleUploadedFile(name='invalidimg.txt', content=img_file.read(), content_type='text/plain')    
            data = {
                'title': 'My first dream',
                'description':'It was horror dream there is so many monsters',
                'is_public':True,
                'image':img,
            } 
            self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.existingusertoken}')
            
            response = self.client.post(self.dream_list_url,data,format='multipart')   
            self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)                    
    
    def test_createPrivateDream(self):
        with open(self.image_path,'rb') as img_file:
            img = SimpleUploadedFile(name='testdreamimg.jpg', content=img_file.read(), content_type='image/jpeg')
            data = {
                'title': 'My first dream',
                'description':'It was horror dream there is so many monsters',
                'image':img,
                'is_public':False,
            } 
            self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.existingusertoken}')
            response = self.client.post(self.dream_list_url,data,format='multipart')   
            self.assertEqual(response.status_code,status.HTTP_201_CREATED)
            self.assertIn('id',response.data)
            self.assertEqual(response.data.get('title'),data.get('title'))
    
    def test_createPublicDream(self):
        with open(self.image_path,'rb') as img_file:
            img = SimpleUploadedFile(name='testdreamimg.jpg', content=img_file.read(), content_type='image/jpeg')
            data = {
                'title': 'My first dream',
                'description':'It was horror dream there is so many monsters',
                'image':img,
                'is_public':True,
            } 
            self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.existingusertoken}')
            
            response = self.client.post(self.dream_list_url,data,format='multipart')   
            self.assertEqual(response.status_code,status.HTTP_201_CREATED)
            self.assertIn('id',response.data)
            self.assertEqual(response.data.get('title'),data.get('title'))        
    
    

class DreamListTests(APITestCase):
    def setUp(self):
        self.image_path = os.path.join( 'media','dream_image', 'testdreamimg.jpg')
        self.loginurl = reverse('login')
        
        #admin user create and login
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
        response = self.client.post(self.loginurl,data)
        self.adminusertoken = response.data.get('access_token')
        
        
        # create a user and login and create dream using that User1
        self.existing_user1 = User(
            first_name = 'Existing',
            last_name = 'User',
            email = 'existinguser@gmail.com',
        )
        self.existing_user1.set_password("Hello@123")
        self.existing_user1.save()
        data = {
            'email': self.existing_user1.email,
            'password':'Hello@123'
        }    
        response = self.client.post(self.loginurl,data)
        self.existingusertoken1 = response.data.get('access_token')
        
        with open(self.image_path,'rb') as img_file:
            img = SimpleUploadedFile(name='testdreamimg.jpg', content=img_file.read(), content_type='image/jpeg')
            self.existing_user1_dream_public = Dream(
                title = 'My first dream u1',
                description='It was horror dream there is so many monsters u1',
                image = img,
                user=self.existing_user1,
                is_public =True      
            )
            self.existing_user1_dream_public.save()
            
            self.existing_user1_dream_private = Dream(
                title = 'My first dream u1',
                description='It was horror dream there is so many monsters u1',
                image = img,
                user=self.existing_user1,
                is_public =False      
            )
            self.existing_user1_dream_private.save()
            
        self.existing_user2 = User(
            first_name = 'Existing',
            last_name = 'User',
            email = 'existinguser2@gmail.com',
        )
        self.existing_user2.set_password("Hello@123")
        self.existing_user2.save()
        data = {
            'email': self.existing_user2.email,
            'password':'Hello@123'
        }    
        response = self.client.post(self.loginurl,data)
        self.existingusertoken2 = response.data.get('access_token')
        
        with open(self.image_path,'rb') as img_file:
            img = SimpleUploadedFile(name='testdreamimg.jpg', content=img_file.read(), content_type='image/jpeg')
            self.existing_user2_dream_public = Dream(
                title = 'My first dream u2',
                description='It was horror dream there is so many monsters u2',
                image = img,
                user=self.existing_user2,
                is_public =True      
            )
            self.existing_user2_dream_public.save()
         
        
        self.dream_detail_url = reverse('dream-detail',kwargs={'pk':self.existing_user1_dream_public.id})
        self.dream_detail_url2 = reverse('dream-detail',kwargs={'pk':self.existing_user2_dream_public.id})
        self.dream_list_url = reverse('dream-list')
        
    
    def test_dream_list_no_auth(self):
        response = self.client.get(self.dream_list_url)    
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)

    def test_dream_list_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer hhhh')
        response = self.client.get(self.dream_list_url)    
        self.assertEqual(response.status_code,status.HTTP_401_UNAUTHORIZED)
        
    def test_user_dream_list(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.existingusertoken1}')
        response = self.client.get(self.dream_list_url,QUERY_STRING='limit=10&offset=1')    
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsInstance(response.data['results'],list)
        usersdreams = [x for x in response.data['results'] if x['user']['id'] == self.existing_user1.id or x['is_public'] == True]
        self.assertEqual(len(usersdreams),len(response.data['results']))
    
    def test_user_dream_list_admin(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.adminusertoken}')
        
        response = self.client.get(self.dream_list_url)    
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsInstance(response.data,list)
        self.assertEqual(len(response.data),Dream.objects.filter(is_active=True).count()) 
    
    def test_user_dream_list_search(self):
        searchkeyword = 'my'
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.existingusertoken1}')
        
        response = self.client.get(self.dream_list_url,QUERY_STRING='search=My')    
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsInstance(response.data,list)
        for dream in response.data:
            assertion = (
                    (searchkeyword in dream['title'].lower()) or 
                    (searchkeyword in dream['description'].lower()) or
                    (searchkeyword in dream['user']['email'].lower()) or
                    (searchkeyword in dream['user']['first_name'].lower()) or
                    (searchkeyword in dream['user']['last_name'].lower())
                    )
            self.assertEqual(assertion,True)
        
        
    def test_user1_dream1_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.existingusertoken1}')
        
        response = self.client.get(self.dream_detail_url)    
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsInstance(response.data,dict)
        self.assertEqual(response.data['id'],self.existing_user1_dream_public.id)
    
    def test_user2_user1_dream1_detail(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.existingusertoken2}')
        
        response = self.client.get(self.dream_detail_url)    
        self.assertEqual(response.status_code,status.HTTP_200_OK)   
    
    def test_user1_dream1_update(self):
        data = {
            'title':'Updated Title'
        }
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.existingusertoken1}')
        
        response = self.client.patch(self.dream_detail_url,data=data)    
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertIsInstance(response.data,dict)
        self.assertEqual(response.data['title'],data.get('title'))
    
    def test_user2_user1_dream1_update(self):
        data = {
            'title':'Updated Title'
        }
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.existingusertoken2}')
        
        response = self.client.patch(self.dream_detail_url,data=data)    
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN) 
    
    def test_user2_user1_dream1_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.existingusertoken2}')
        
        response = self.client.delete(self.dream_detail_url)    
        self.assertEqual(response.status_code,status.HTTP_403_FORBIDDEN)  
        
    
    def test_user1_dream1_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.existingusertoken1}')
        
        response = self.client.delete(self.dream_detail_url)    
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)     
        
    def test_admin_user2_dream1_delete(self):
        self.client.credentials(HTTP_AUTHORIZATION = f'Bearer {self.adminusertoken}')
        
        response = self.client.delete(self.dream_detail_url2)    
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)    
             
    
               