from rest_framework import serializers
from dream.models import Dream,DreamLikes
from customauth.api.serializers import UserSerializer

class DreamSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    total_likes = serializers.IntegerField(read_only=True)
    total_dislikes = serializers.IntegerField(read_only=True)
    
    is_user_liked = serializers.BooleanField(read_only=True)
    is_user_disliked = serializers.BooleanField(read_only=True)
    class Meta:
        model = Dream
        fields = '__all__'

class DreamLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DreamLikes
        fields = '__all__'      

    