from rest_framework import serializers
from .models import Customuserprofile, Customuser

class UserprofileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuserprofile
        fields = "__all__"

class CustomuserSerializer(serializers.ModelSerializer):
    user_profile = UserprofileSerializer()
    class Meta:
        model = Customuser
        fields = ("email", "username", "created_at", "updated_at", "user_profile")
