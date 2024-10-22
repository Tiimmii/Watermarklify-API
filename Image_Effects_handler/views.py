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
from django.core.files.images import ImageFile
from PIL import Image
from .cloudinary import upload_to_cloudinary
import ast
import os
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
                "image_type": Effects.get_image_type(image, ">"),
                "image_url": image.image,
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
        UserImages.objects.create_image(user=user, **serializer.validated_data)
        image = UserImages.objects.filter(user=user).first()
        user_images = []
        user_images.append({
                "image_id": image.id,
                "name": image.name,
                "image_type": Effects.get_image_type(image, ">"),
                "image_url": image.image,
                "created_at": image.created_at,
                "updated_at": image.updated_at,
            })
        return Response({
            "data": "Uploaded successfully",
            "user_images_data": user_images 
        }, status.HTTP_200_OK)

class Handle_Image_Effects(GenericAPIView):
    serializer_class = HandleUserImagesSerializer
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
                "image_type": Effects.get_image_type(user_image, ">"),
                "image_url": user_image.image,
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
        user = request.user
        try:
            user_image = self.get_object(pk)
        except Exception as e:
            raise Exception(f"error {e}")
        
        old_public_id = user_image.public_id
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        s = serializer.validated_data
        s["user"] = user
        image_effects = s.get("image_effects", {})
        R = Response({"data":"No Effect Applied Successfully"}, status=status.HTTP_200_OK)
        if not image_effects:
            return R
        else:
            if "add_border" in image_effects:
                e = image_effects["add_border"]
                # Apply border, then upload to Cloudinary
                patched_image = Effects.add_border(user_image.image, e["left"], e["top"], e["right"], e["bottom"], ast.literal_eval(e["border_color"]), Effects.get_image_type(user_image, ">"))
                patched_image_url = upload_to_cloudinary(patched_image, old_public_id)  # Re-upload the modified image to Cloudinary
                user_image.image = patched_image_url[0]
                user_image.public_id = patched_image_url[1]
                old_public_id = user_image.public_id
                user_image.save()

            if "crop_image" in image_effects:
                e = image_effects["crop_image"]
                cropped_image = Effects.crop_image(user_image.image, e["start_x"], e["start_y"], e["end_x"], e["end_y"], Effects.get_image_type(user_image, ">"))
                cropped_image_url = upload_to_cloudinary(cropped_image, old_public_id)  # Re-upload the cropped image
                user_image.image = cropped_image_url[0]
                user_image.public_id = cropped_image_url[1]
                old_public_id = user_image.public_id
                user_image.save()

            if "rotate_image" in image_effects:
                e = image_effects["rotate_image"]
                rotated_image = Effects.rotate_image(user_image.image, e["degrees"], e["flip_horizontal"], e["flip_vertical"], Effects.get_image_type(user_image, ">"))
                rotated_image_url = upload_to_cloudinary(rotated_image, old_public_id)  # Re-upload the rotated image
                user_image.image = rotated_image_url[0]
                user_image.public_id = rotated_image_url[1]
                old_public_id = user_image.public_id
                user_image.save()

            if "resize_image" in image_effects:
                e = image_effects["resize_image"]
                resized_image = Effects.resize_image(user_image.image, e["width"], e["height"], e["width_unit"], e["height_unit"], e["mode"], e["aspect_ratio"], Effects.get_image_type(user_image, ">"))
                resized_image_url = upload_to_cloudinary(resized_image, old_public_id)  # Re-upload the resized image
                user_image.image = resized_image_url[0]
                user_image.public_id = resized_image_url[1]
                old_public_id = user_image.public_id
                user_image.save()

            if "adjust_exposure" in image_effects:
                e = image_effects["adjust_exposure"]
                adjusted_exposure = Effects.adjust_exposure(user_image.image, e["contrast_factor"], e["brightness_factor"], Effects.get_image_type(user_image, ">"))
                adjusted_exposure_url = upload_to_cloudinary(adjusted_exposure, old_public_id)  # Re-upload the image with adjusted exposure
                user_image.image = adjusted_exposure_url[0]
                user_image.public_id = adjusted_exposure_url[1]
                old_public_id = user_image.public_id
                user_image.save()

            if "apply_filter" in image_effects:
                e = image_effects["apply_filter"]
                filtered_image = Effects.apply_filter(user_image.image, e["filter_name"], Effects.get_image_type(user_image, ">"))
                filtered_image_url = upload_to_cloudinary(filtered_image, old_public_id)  # Re-upload the image with applied filter
                user_image.image = filtered_image_url[0]
                user_image.public_id = filtered_image_url[1]
                old_public_id = user_image.public_id
                user_image.save()

            if "convert_image_type" in image_effects:
                e = image_effects["convert_image_type"]
                converted_image = Effects.convert_image_type(user_image.image, e["type"])
                converted_image_url = upload_to_cloudinary(converted_image, old_public_id)
                user_image.image = converted_image_url[0]
                user_image.public_id = converted_image_url[1]
                old_public_id = user_image.public_id
                user_image.save()

            response_data = {
                "data": "Effect Applied Successfully",
                "new_image_data": {
                    "image_id": user_image.id,
                    "name": user_image.name,
                    "image_type": Effects.get_image_type(user_image, ">"),
                    "image_url": user_image.image,
                    "created_at": user_image.created_at,
                    "updated_at": user_image.updated_at
                }
            }
        return Response(response_data, status=status.HTTP_200_OK)




            
            
