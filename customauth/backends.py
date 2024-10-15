from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model

User = get_user_model()
class EmailBackend(BaseBackend):
    def authenticate(self, request, username, password,**kwargs):
        try:
            user = User.objects.get(email = username)
            validate_password = user.check_password(password)
            if not validate_password:
                return None
            return user
        except User.DoesNotExist:
            return None  
    
    def get_user(self, user_id):
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            return None    