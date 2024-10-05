from PIL import Image, ImageOps
import os
from CustomUser.models import Customuser
from .models import Image

class Effects():
    def add_border(image, left, top, right, bottom, border_color=(0, 0, 0)):
        try:
            return ImageOps.expand(image, (left, top, right, bottom), fill=border_color)

        except Exception:
            raise Exception("Unable to place borders. Check image, left, top, right, bottom, border_color")
    
    def crop_image(image, start_x, start_y, end_x, end_y):
        try:
          return image.crop((start_x, start_y, end_x, end_y))
        except Exception:
            raise Exception("Unable to crop image. Check image, start_x, start_y, end_x, end_y")
        
    def adjust_exposure(image_path, contrast_factor, brightness_factor):
        contrast = ImageEnhance.Contrast(img)
        img = contrast.enhance(contrast_factor)

        # Adjust brightness
        brightness = ImageEnhance.Brightness(img)
        img = brightness.enhance(brightness_factor)