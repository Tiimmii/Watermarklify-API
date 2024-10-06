from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import CreateNewImageSerializer, HandleUserImagesSerializer
from rest_framework.permissions import IsAuthenticated
from gateway.authentication import Authentication
from .models import UserImages
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from .Handle_Effects import Effects
from django.http import Http404
# Create your views here.


class Image_Effects(GenericAPIView):
    # authentication_classes = [Authentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = CreateNewImageSerializer
    h_serizlizer = HandleUserImagesSerializer
    def get(self, request):
        user = request.user
        images = UserImages.objects.filter(user=user)
        user_images = []
        for image in images:
            user_images.append({
                "image_id": image.id,
                "name": image.name,
                "image_type": Effects.get_image_type(image),
                "image_url": request.build_absolute_uri(image.image.url),
                "created_at": image.created_at,
                "updated_at": image.updated_at,
            })
        return Response({
        "user": {
            "username": user.username,
            "email": user.email
        },
        "user_images_data": user_images 
        })
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        UserImages.objects.create(user=user, **serializer.validated_data)
        return Response({
            "data": "Uploaded successfully"
        }, status.HTTP_200_OK)

class Handle_Image_Effects(GenericAPIView):
    def get_object(self, pk):
        try:
            return UserImages.objects.get(id=pk)
        except:
            raise Http404
    def get(self, request, pk):
        user_image = self.get_object(pk)
        user_images = []
        user_images.append({
                "image_id": user_image.id,
                "name": user_image.name,
                "image_type": Effects.get_image_type(user_image),
                "image_url": request.build_absolute_uri(user_image.image.url),
                "created_at": user_image.created_at,
                "updated_at": user_image.updated_at,
            })
        return Response({
            "user": {
            "username": user_image.user.username,
            "email": user_image.user.email
        },
        "images_data":  user_images
        })
    def patch(self, request, pk):
        pass