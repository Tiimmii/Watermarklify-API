from django.shortcuts import render
from .models import Jwt
from CustomUser.models import Customuser
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import LoginSerializer, RegisterSerializer, RefreshSerializer, RequestPasswordResetEmailSerializer, SetNewPasswordSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .authentication import Authentication, Get_token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework import status
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util


# Create your views here.
class Loginview(APIView):
    serializer_class = LoginSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username_or_email = serializer.validated_data['username_or_email']
        password = serializer.validated_data['password']
        user = None
        try:
            # Try to fetch the user by username or email
            user = Customuser.objects.get(
                Q(username__iexact=username_or_email) |
                Q(email__iexact=username_or_email.lower())
            )
        except Customuser.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=400)
        
        user = authenticate(username=user.username, password=password)
        
        if not user:
            return Response({"error": "Invalid credentials"}, status=400)
        Jwt.objects.filter(user_id=user.id).delete()

        access = Get_token.get_access_token({"user":user.id})
        refresh = Get_token.get_refresh_token()

        Jwt.objects.create(user_id = user.id, access_token = access, refresh_token= refresh)
        #decode() removes the b' which may prevent validation    
        return Response({"access_token":access, "refresh_token": refresh})
        #here the JSON decodes automatically

class Registerview(APIView):
    serializer_class = RegisterSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        Customuser.objects.create_user(**serializer.validated_data)

        return Response({"success": "user created."}, status=200)
    

class Refreshview(APIView):
    serializer_class = RefreshSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            active_jwt=Jwt.objects.get(refresh_token=serializer.validated_data["refresh_token"])
        except Jwt.DoesNotExist:
            return Response({"error": "refresh token not found"}, status="400")
        
        if not Authentication.valid_token(active_jwt.refresh_token):
            return Response({"error": "token not valid or expired"}, status="400")
        
        access_token = Get_token.get_access_token({"user_id":active_jwt.user.id})
        refresh_token = Get_token.get_refresh_token()

        active_jwt.access_token = access_token
        active_jwt.refresh_token = refresh_token
        active_jwt.save()

        return Response({"access_token":access_token, "refresh_token": refresh_token}, status="200")

class Getsecuredinfo(APIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request.user)
        return Response({"data": "this is a secured info"}, status="200")
    
class RequestPasswordResetEmail(GenericAPIView):
    serializer_class = RequestPasswordResetEmailSerializer
    def post(self, request):
        serializer = self.serializer_class(data = request.data) 
        user =  Customuser.objects.filter(email=request.data['email'])
        if user.exists():
            user = user.first()
            uibd64 =  urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request).domain
            relativeLink = reverse('password-reset-confirm', kwargs={'uidb64': uibd64, 'token': token})
            absurl = 'http://'+current_site+relativeLink
            email_body = 'Hi '+user.username + \
                ' Use the link below to reset your password \n' + absurl
            data = {'email_body': email_body, 'to_email': user.email,
                    'email_subject': 'Reset Your Password'}

            Util.send_email(data)
        return Response({'success': 'We have sent you a link to reset your password'}, status = status.HTTP_200_OK)

class PasswordTokenCheckAPI(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = Customuser.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({'error': 'Token not valid anymore'}, status=status.HTTP_401_UNAUTHORIZED)
            
            return Response({'success': True, 'message': 'credentials_valid', 'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)
            
        except DjangoUnicodeDecodeError:
            if not PasswordResetTokenGenerator().check_token(user):
                return Response({'error': 'Token not valid anymore'}, status=status.HTTP_401_UNAUTHORIZED)
            
class SetNewPassword(GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'success':True, 'message': 'password reset success'}, status=status.HTTP_200_OK)
   
