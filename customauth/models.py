from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

class UserManager(BaseUserManager):
    def creat_user(self,email,first_name,last_name,password=None):
        if not email:
            raise ValueError("Email is required")
        if not first_name:
            raise ValueError("first_name is required") 
        if not password:
            raise ValueError("password is required") 
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self,email,first_name,last_name,password=None):
        if not email:
            raise ValueError("Email is required")
        if not first_name:
            raise ValueError("first_name is required") 
        if not password:
            raise ValueError("password is required") 
        email = self.normalize_email(email)
        user = self.model(email=email,first_name=first_name,last_name=last_name)
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.save()
        return user
        

# Create your models here.
class User(AbstractBaseUser):
    first_name = models.CharField(max_length=200,null=False,blank=False)
    last_name = models.CharField(max_length=100,null=False,blank=False)
    email = models.EmailField(max_length=255,null=False,blank=False,unique=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin
    
    def has_module_perms(self, app_label):
        return True
    