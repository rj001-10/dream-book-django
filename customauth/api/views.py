from rest_framework.views import APIView
from customauth.api.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework import status
import json
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from customauth.models import User
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from customauth.api.permissions import IsAdminOrLoggedInUser

with open('utils/lang/en.json','r') as f:
    en = json.load(f)

class SignupView(APIView):
    
    def post(self,request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': en['AUTH_API']['SIGNUP_SUCCESS']
            },status=status.HTTP_201_CREATED)
        else:
            return Response({
                'errors':serializer.errors 
            },status=status.HTTP_400_BAD_REQUEST)
            
            
class LoginView(APIView):
    
    def post(self,request):
        email = request.data.get('email')   
        password = request.data.get('password')   
        if not email or not password:
            return Response({'Error':en['AUTH_API']['SIGNUP_REQUIRED_FIELDS']},status=status.HTTP_400_BAD_REQUEST)
        
        user = authenticate(username = email,password=password)
        
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'access_token': str(refresh.access_token),
                'refresh_token': str(refresh),
            },status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)   

class DeleteUserView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated,IsAdminOrLoggedInUser]
    
        
            
            