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
        UserImages.objects.create_image(user=user, **serializer.validated_data)
        image = UserImages.objects.filter(user=user).first()
        user_images = []
        user_images.append({
                "image_id": image.id,
                "name": image.name,
                "image_type": Effects.get_image_type(image, ">"),
                "image_url": request.build_absolute_uri(image.image.url),
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
        user = request.user
        try:
            user_image = self.get_object(pk)
        except Exception as e:
            raise Exception(f"error {e}")
        user_images = []
        user_images.append({
                "image_id": user_image.id,
                "name": user_image.name,
                "image_type": Effects.get_image_type(user_image, ">"),
                "image_url": request.build_absolute_uri(user_image.image.url),
                "created_at": user_image.created_at,
                "updated_at": user_image.updated_at,
            })
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        s = serializer.validated_data
        s["user"] = user
        image_effects = s.get("image_effects", {})
        R = Response({"data":"Effect Applied Successfully", "image_data":user_images}, status=status.HTTP_200_OK)
        if not image_effects:
            return R
        else:
            if "add_border" in image_effects:
                e = image_effects["add_border"]
                patched_image = Effects.add_border(user_image.image.path, e["left"], e["top"], e["right"], e["bottom"], ast.literal_eval(e["border_color"]))
                patched_image.save(user_image.image.path)
                response_data = {
                    "data": "Effect Applied Successfully",
                    "new_image_data": {
                        "image_id": user_image.id,
                        "name": user_image.name,
                        "image_type": Effects.get_image_type(user_image, ">"),  # Get the new image type
                        "image_url": new_image_url,  # New image URL
                        "created_at": user_image.created_at,
                        "updated_at": user_image.updated_at
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)
            if "crop_image" in image_effects:
                e = image_effects["crop_image"]
                cropped_image = Effects.crop_image(user_image.image.path, e["start_x"], e["start_y"], e["end_x"], e["end_y"])
                cropped_image.save(user_image.image.path)
                response_data = {
                    "data": "Effect Applied Successfully",
                    "new_image_data": {
                        "image_id": user_image.id,
                        "name": user_image.name,
                        "image_type": Effects.get_image_type(user_image, ">"),  # Get the new image type
                        "image_url": new_image_url,  # New image URL
                        "created_at": user_image.created_at,
                        "updated_at": user_image.updated_at
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)
            if "rotate_image" in image_effects:
                e = image_effects["rotate_image"]
                rotated_image = Effects.rotate_image(user_image.image.path, e["degrees"], e["flip_horizontal"], e["flip_vertical"])
                rotated_image.save(user_image.image.path)
                response_data = {
                    "data": "Effect Applied Successfully",
                    "new_image_data": {
                        "image_id": user_image.id,
                        "name": user_image.name,
                        "image_type": Effects.get_image_type(user_image, ">"),  # Get the new image type
                        "image_url": new_image_url,  # New image URL
                        "created_at": user_image.created_at,
                        "updated_at": user_image.updated_at
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)
            if "resize_image" in image_effects:
                e = image_effects["resize_image"]
                if e["aspect_ratio"]!=None:
                    resized_image = Effects.resize_image(user_image.image.path, e["width"], e["height"], e["width_unit"], e["height_unit"], e["mode"], e["aspect_ratio"])
                else:
                    resized_image = Effects.resize_image(user_image.image.path, e["width"], e["height"], e["width_unit"], e["height_unit"], e["mode"])
                resized_image.save(user_image.image.path)
                response_data = {
                    "data": "Effect Applied Successfully",
                    "new_image_data": {
                        "image_id": user_image.id,
                        "name": user_image.name,
                        "image_type": Effects.get_image_type(user_image, ">"),  # Get the new image type
                        "image_url": new_image_url,  # New image URL
                        "created_at": user_image.created_at,
                        "updated_at": user_image.updated_at
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)
            if "adjust_exposure" in image_effects:
                e = image_effects["adjust_exposure"]
                adjusted_exposure = Effects.adjust_exposure(user_image.image.path, e["contrast_factor"], e["brightness_factor"])
                adjusted_exposure.save(user_image.image.path)
                response_data = {
                    "data": "Effect Applied Successfully",
                    "new_image_data": {
                        "image_id": user_image.id,
                        "name": user_image.name,
                        "image_type": Effects.get_image_type(user_image, ">"),  # Get the new image type
                        "image_url": new_image_url,  # New image URL
                        "created_at": user_image.created_at,
                        "updated_at": user_image.updated_at
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)
            if "apply_filter" in image_effects:
                e = image_effects["apply_filter"]
                filtered_image = Effects.apply_filter(user_image.image.path, e["filter_name"])
                filtered_image.save(user_image.image.path)
                response_data = {
                    "data": "Effect Applied Successfully",
                    "new_image_data": {
                        "image_id": user_image.id,
                        "name": user_image.name,
                        "image_type": Effects.get_image_type(user_image, ">"),  # Get the new image type
                        "image_url": new_image_url,  # New image URL
                        "created_at": user_image.created_at,
                        "updated_at": user_image.updated_at
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)
            if "convert_image_type" in image_effects:
                e = image_effects["convert_image_type"]
                
                # Store the old image path before overwriting the image
                old_image_path = user_image.image.path if user_image.image else None
                
                # Open the current image file before it's deleted
                if old_image_path:
                    with open(old_image_path, 'rb') as image_file:
                        # Save the new image with the new type
                        user_image.image.save('converted_image' + "." + e["type"], ContentFile(image_file.read()), save=False)
                
                user_image.save()  # Save the updated instance
                
                # After saving the new image, delete the old image file
                if old_image_path:
                    os.remove(old_image_path)  # Delete the old image file from the system
                
                new_image_url = request.build_absolute_uri(user_image.image.url)
                response_data = {
                    "data": "Effect Applied Successfully",
                    "new_image_data": {
                        "image_id": user_image.id,
                        "name": user_image.name,
                        "image_type": Effects.get_image_type(user_image, ">"),  # Get the new image type
                        "image_url": new_image_url,  # New image URL
                        "created_at": user_image.created_at,
                        "updated_at": user_image.updated_at
                    }
                }
                return Response(response_data, status=status.HTTP_200_OK)




            
            
