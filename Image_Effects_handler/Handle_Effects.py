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
        try:
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
            return img
        except Exception:
            raise Exception("Unable to rotate Image. Check img, degrees, flip_horizontal, flip_vertical")
        
    def resize_image(img, width, height, width_unit='px', height_unit='px', mode='contain', aspect_ratio=None):
        try:
            original_width, original_height = img.size
        
            # Calculate the new dimensions
            def calculate_dimension(dimension, unit, original_dimension):
                if unit == 'px':
                    return dimension
                elif unit == '%':
                    return int(original_dimension * (dimension / 100))
                else:
                    raise ValueError("Invalid unit, must be 'px' or '%'")

            new_width = calculate_dimension(width, width_unit, original_width)
            new_height = calculate_dimension(height, height_unit, original_height)

            # Maintain aspect ratio if specified
            if aspect_ratio:
                aspect_w, aspect_h = map(int, aspect_ratio.split(':'))
                ratio = aspect_w / aspect_h
                if new_width / new_height > ratio:
                    new_width = int(new_height * ratio)
                else:
                    new_height = int(new_width / ratio)
            
            # Handle resize modes
            if mode == 'stretch':
                img = img.resize((new_width, new_height))
            elif mode == 'contain':
                img = img.resize((new_width, new_height), Image.LANCZOS)
                # Ensure the image is centered if it's being contained
                canvas = Image.new('RGB', (new_width, new_height), (255, 255, 255))
                img_width, img_height = img.size
                offset = ((new_width - img_width) // 2, (new_height - img_height) // 2)
                canvas.paste(img, offset)
                img = canvas
            elif mode == 'trim':
                img = img.crop((0, 0, new_width, new_height))
            else:
                raise ValueError("Mode must be 'trim', 'stretch', or 'contain'")
            
            return img
        except Exception:
            raise Exception("Unable to resize Image. Check img, width, height, width_unit, height_unit, mode, aspect_ratio")
        
    def apply_filter(img, filter_name):
        def apollo(img):
            img = ImageEnhance.Contrast(img).enhance(1.5)  # Increase contrast
            green_overlay = Image.new('RGB', img.size, (144, 238, 144))  # Light green overlay
            img = Image.blend(img, green_overlay, 0.2)
            return img

        # Brannan: Warm tone with high contrast and saturation
        def brannan(img):
            img = ImageEnhance.Contrast(img).enhance(1.3)  # Increase contrast
            img = ImageEnhance.Color(img).enhance(1.4)     # Increase saturation
            warm_overlay = Image.new('RGB', img.size, (153, 102, 51))  # Warm tone overlay
            img = Image.blend(img, warm_overlay, 0.1)
            return img

        # Earlybird: Sepia tone with soft highlights
        def earlybird(img):
            img = ImageEnhance.Brightness(img).enhance(1.1)  # Brighten the image slightly
            img = ImageEnhance.Color(img).enhance(0.6)       # Desaturate the image
            sepia = ImageOps.colorize(img.convert('L'), '#704214', '#FFDAB9')  # Sepia tone
            return sepia

        # Gotham: High contrast, blue desaturation
        def gotham(img):
            img = ImageEnhance.Contrast(img).enhance(1.6)  # High contrast
            img = ImageEnhance.Color(img).enhance(0.3)     # Desaturate slightly
            blue_overlay = Image.new('RGB', img.size, (32, 64, 128))  # Cool blue overlay
            img = Image.blend(img, blue_overlay, 0.2)
            return img

        # Hefe: Warm, saturated with high contrast
        def hefe(img):
            img = ImageEnhance.Contrast(img).enhance(1.5)
            img = ImageEnhance.Color(img).enhance(1.4)
            warm_overlay = Image.new('RGB', img.size, (255, 140, 0))  # Warm orange overlay
            img = Image.blend(img, warm_overlay, 0.1)
            return img

        # Kelvin: Bright yellowish tone
        def kelvin(img):
            img = ImageEnhance.Brightness(img).enhance(1.3)
            img = ImageEnhance.Color(img).enhance(1.6)
            yellow_overlay = Image.new('RGB', img.size, (255, 255, 102))  # Yellow tone
            img = Image.blend(img, yellow_overlay, 0.2)
            return img

        # Inkwell: Black and white with high contrast
        def inkwell(img):
            img = img.convert('L')  # Convert to grayscale
            img = ImageEnhance.Contrast(img).enhance(1.8)  # Increase contrast
            return img

        # Lomo: Warm vintage with high contrast
        def lomo(img):
            img = ImageEnhance.Contrast(img).enhance(1.6)
            warm_overlay = Image.new('RGB', img.size, (255, 140, 0))  # Warm overlay
            img = Image.blend(img, warm_overlay, 0.2)
            img = ImageOps.vignette(img)  # Add vignette effect
            return img
        try:
            # Apply the selected filter
            if filter_name.lower() == 'apollo':
                apollo(img)
            elif filter_name.lower() == 'brannan':
                brannan(img)
            elif filter_name.lower() == 'earlybird':
                earlybird(img)
            elif filter_name.lower() == 'gotham':
                gotham(img)
            elif filter_name.lower() == 'hefe':
                hefe(img)
            elif filter_name.lower() == 'kelvin':
                kelvin(img)
            elif filter_name.lower() == 'inkwell':
                inkwell(img)
            elif filter_name.lower() == 'lomo':
               lomo(img)
            else:
                raise ValueError("Invalid filter name. Please choose Apollo, Brannan, Earlybird, Gotham, Hefe, Kelvin, Inkwell, or Lomo.")
        except Exception:
             raise Exception("Unable to apply filter to Image. img, filter_name")

