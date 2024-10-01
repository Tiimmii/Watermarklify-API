from rest_framework import serializers
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


class LoginSerializer(serializers.Serializer):
    username_or_email = serializers.CharField()
    password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField()
    password = serializers.CharField()

class RefreshSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

class RequestPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length = 2)

    class meta:
        fields = ['email']

    def validate(self, attrs):
        email = attrs['data'].get('email', '')

class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=4, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)

    class meta:
        fields = ['password', 'uidb64', 'token']

    def validate(self, attrs):
        try:
            
        except:
            pass

        