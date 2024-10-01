from rest_framework import serializers
from .models import Customuser
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util

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
        try:
            email = attrs['data'].get('email', '')
            user =  Customuser.objects.filter(email=email)
            if user.exists():
                uibd64 =  urlsafe_base64_encode(user.id)
                token = PasswordResetTokenGenerator().make_token(user)
                current_site = get_current_site(attrs['data'].get('request')).domain
                relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uibd64, 'token': token})
                absurl = 'http://'+current_site+relativeLink
                email_body = 'Hi '+user.username + \
                    ' Use the link below to reset your password \n' + absurl
                data = {'email_body': email_body, 'to_email': user.email,
                        'email_subject': 'Reset Your Password'}

                Util.send_email(data)
                return attrs
        except:
            pass