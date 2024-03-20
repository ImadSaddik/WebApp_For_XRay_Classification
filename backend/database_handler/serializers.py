from rest_framework import serializers

from djoser.serializers import UserCreateSerializer
from django.contrib.auth import get_user_model

from .models import PatientImage

class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = get_user_model()
        fields = ('id', 'email', 'name', 'password')
        
        
class PatientImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientImage
        fields = (
            "image_id",
            "classification",
            "getImage",
        )
