from rest_framework import serializers
from CustomUser.models import Customuser
from .models import UserImages

class CreateNewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserImages
        fields = ['name','image']
    
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customuser
        fields = ['id', 'username', 'email']

class AddBorderSerializer(serializers.Serializer):
    left = serializers.IntegerField(required=True)
    top = serializers.IntegerField(required=True)
    right = serializers.IntegerField(required=True)
    bottom = serializers.IntegerField(required=True)
    border_color = serializers.CharField(required=True, allow_blank=False)

# Serializer for the crop_image action
class CropImageSerializer(serializers.Serializer):
    start_x = serializers.IntegerField(required=True)
    start_y = serializers.IntegerField(required=True)
    end_x = serializers.IntegerField(required=True)
    end_y = serializers.IntegerField(required=True)

class RotateImageSerializer(serializers.Serializer):
    degrees = serializers.IntegerField(required=True)
    flip_horizontal = serializers.BooleanField(required=True)
    flip_vertical = serializers.BooleanField(required=True)

class ResizeImageSerializer(serializers.Serializer):
    width = serializers.IntegerField(required=True)
    height = serializers.IntegerField(required=True)
    width_unit = serializers.ChoiceField(choices=[("px", "px"), ("%", "%")], required=True)
    height_unit = serializers.ChoiceField(choices=[("px", "px"), ("%", "%")], required=True)
    mode = serializers.ChoiceField(choices=[("contain", "contain"), ("stretch", "stretch"), ("trim", "trim")], required=False)
    aspect_ratio = serializers.ChoiceField(choices=[("1:1","1:1"),("4:3", "4:3"),("3:2", "3:2"),("16:9","16:9"),("2:1","2:1")], required=False)

class AdjustImageExposureSerializer(serializers.Serializer):
    contrast_factor = serializers.IntegerField(required=True)
    brightness_factor = serializers.IntegerField(required=True)

class ApplyFilterSerializer(serializers.Serializer):
    filter_name = serializers.CharField(required=True, allow_blank = False)

class ConvertImageTypeSerializer(serializers.Serializer):
    type = serializers.CharField(required=True, allow_blank = False)    

# Serializer for handling the image_effects field, which includes add_border and crop_image
class ImageEffectsSerializer(serializers.Serializer):
    add_border = AddBorderSerializer(required=False)
    crop_image = CropImageSerializer(required=False)
    rotate_image = RotateImageSerializer(required=False)
    resize_image = ResizeImageSerializer(required=False)
    adjust_exposure = AdjustImageExposureSerializer(required=False)
    apply_filter = ApplyFilterSerializer(required=False)
    convert_image_type = ConvertImageTypeSerializer(required=False)

class HandleUserImagesSerializer(serializers.Serializer):
    user = UserSerializer
    image_effects = ImageEffectsSerializer(required=False)

    class meta:
        fields = ['image_effects']
