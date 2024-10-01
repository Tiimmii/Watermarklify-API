from django.shortcuts import render
from .models import Jwt
from CustomUser.models import Customuser
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from .serializers import LoginSerializer, RegisterSerializer, RefreshSerializer, RequestPasswordResetEmailSerializer
from django.contrib.auth import authenticate
from rest_framework.response import Response
from .authentication import Authentication, Get_token
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

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
        data = {"request": request, "data": request.data}
        serializer = self.serializer_class(data = data)
        serializer.is_valid(raise_exception=True)

class PasswordTokenCheckAPI(GenericAPIView):
    def get(self, request, uidb64, token):
        pass

