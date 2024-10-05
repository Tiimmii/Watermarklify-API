from rest_framework import serializers
from CustomUser.models import Customuser
from .models import UserImages

class CreateNewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImages
        fields = ['image']

class HandleUserImagesSerializer(serializers.Serializer):
    pass