from PIL import ImageOps, ImageEnhance, Image
import os
from CustomUser.models import Customuser
from .models import UserImages

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
        
    def adjust_exposure(image, contrast_factor, brightness_factor):
        try:
            contrast = ImageEnhance.Contrast(image)
            img = contrast.enhance(contrast_factor)

            # Adjust brightness
            brightness = ImageEnhance.Brightness(img)
            img = brightness.enhance(brightness_factor)

            return img
        except:
            raise Exception("Unable to adjust exposure. Check image, contrast_factor, brightness_factor")
        
    def rotate_image(img, degrees, flip_horizontal=False, flip_vertical=False):
        # Normalize degrees to the left or right in 90-degree increments
        if degrees % 90 != 0:
            raise ValueError("Degrees should be a multiple of 90")

        # Determine the direction of rotation
        if degrees < 0:
            # Left rotation
            num_rotations = abs(degrees) // 90
            for _ in range(num_rotations):
                img = img.rotate(90, expand=True)
        else:
            # Right rotation
            num_rotations = degrees // 90
            for _ in range(num_rotations):
                img = img.rotate(-90, expand=True)

        # Apply flipping if necessary
        if flip_horizontal:
            img = img.transpose(Image.FLIP_LEFT_RIGHT)
        
        if flip_vertical:
            img = img.transpose(Image.FLIP_TOP_BOTTOM)

        # Save the rotated and flipped image
        img.save(output_path)
        print(f"Image saved to {output_path}")