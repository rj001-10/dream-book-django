from rest_framework import serializers
from customauth.models import User

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['email','first_name','last_name','password','password2','id']
        extra_kwargs = { 'password':{'write_only':True} }
    
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']
        
        if password != password2:
            raise serializers.ValidationError({'Error':'Password miss match'})
        
        user = User(
            email = self.validated_data['email'],
            first_name = self.validated_data['first_name'],
            last_name = self.validated_data['last_name'],
            )
        user.set_password(self.validated_data['password'])
        user.save()
        return user