from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import CreateNewImageSerializer, HandleUserImagesSerializer
from rest_framework.permissions import IsAuthenticated
from gateway.authentication import Authentication
from .models import UserImages
from rest_framework.response import Response
# Create your views here.


class Image_Effects(GenericAPIView):
    authentication_classes = [Authentication]
    permission_classes = [IsAuthenticated]
    c_serializer = CreateNewImageSerializer
    h_serizlizer = HandleUserImagesSerializer
    def get(self, request):
        return Response()
    def post(self, request):
        user = request.user
        serializer = self.c_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)
        UserImages.objects.create(user=user, **serializer.validated_data)

