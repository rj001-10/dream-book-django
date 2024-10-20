from django.db import models
from customauth.models import User
import os
import time
from django.core.validators import validate_image_file_extension
# Create your models here.
def unique_image_path(instance, filename):
    ext = filename.split('.')[-1]
    unique_filename = f"dream_{instance.user.id}_{int(time.time())}.{ext}"
    return os.path.join('dream_image/', unique_filename)



class Dream(models.Model):
    title = models.CharField(max_length=255,null=False,blank=False)
    description = models.TextField(blank=False,null=False)
    image = models.ImageField(upload_to=unique_image_path,null=True,blank=True,validators=[validate_image_file_extension])
    user = models.ForeignKey(User,related_name='dreams',on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    is_public = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title


class DreamLikes(models.Model):
    dream = models.ForeignKey(Dream,on_delete=models.CASCADE,related_name='dreamlikes') 
    is_like = models.BooleanField(default=False,null=True,blank=True)   
    is_dislike = models.BooleanField(default=False,null=True,blank=True)   
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    
    def __str__(self):
        modelstring = f'{self.user.first_name} - {self.dream.title}'
        if self.is_like:
            modelstring += ' Liked'
        
        if self.is_dislike:
            modelstring += ' DisLiked'    
        return modelstring