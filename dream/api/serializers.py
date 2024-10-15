from rest_framework import serializers
from dream.models import Dream
from customauth.api.serializers import UserSerializer

class DreamSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Dream
        fields = '__all__'
    