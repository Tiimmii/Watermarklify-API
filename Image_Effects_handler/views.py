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
# Create your views here.


class Image_Effects(GenericAPIView):
    # authentication_classes = [Authentication]
    # permission_classes = [IsAuthenticated]
    serializer_class = CreateNewImageSerializer
    # h_serizlizer = HandleUserImagesSerializer
    def get(self, request):
        user = request.user
        images = UserImages.objects.filter(user=user)
        user_images = []
        for image in images:
            result = Effects.get_image_type(image)
            image_name = image.name  # Getting the image file name
            image_url = request.build_absolute_uri(image.image.url)  # Full URL to the image
            user_images.append({
                "name": image_name,
                "image_type": result,
                "image_url": image_url,
                "created_at": image.created_at,
                "updated_at": image.updated_at,
            })
        return Response({
        "user": {
            "username": user.username,
            "email": user.email
        },
        "user_images": user_images  # Return a list of images
        })
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data = request.data)
        serializer.is_valid(raise_exception=True)
        UserImages.objects.create(user=user, **serializer.validated_data)

