from PIL import ImageOps, ImageEnhance, Image
from django.conf import settings
import io
from io import BytesIO
import requests


class Effects():
    @staticmethod
    def add_border(image, left, top, right, bottom, border_color=(0, 0, 0)):
        try:
            response = requests.get(image)
            response.raise_for_status()  # Check if the request was successful
        except requests.exceptions.RequestException as e:
            print(f"Error downloading image: {e}")
            raise Exception("Unable to download image from the URL.")
        
        try:
            img = Image.open(BytesIO(response.content))
            print("byte worked")
        except Exception as e:
            print(f"Error opening image: {e}")
            raise Exception("Unable to open image.")
        
        try:
            img_with_border = ImageOps.expand(img, (left, top, right, bottom), fill=border_color)
            img_with_border=img_with_border.convert('RGB')
            img_bytes = io.BytesIO()
            img_with_border.save(img_bytes, format='JPEG') 
            img_bytes.seek(0)
            return img_bytes
        except Exception as e:
            print(f"Error: {e}")
            raise Exception("Unable to place borders. Check image, left, top, right, bottom, border_color")
    @staticmethod
    def crop_image(image, start_x, start_y, end_x, end_y):
        img = Image.open(image)
        try:
          return image.crop((start_x, start_y, end_x, end_y))
        except Exception:
            raise Exception("Unable to crop image. Check image, start_x, start_y, end_x, end_y")
    @staticmethod    
    def adjust_exposure(image, contrast_factor, brightness_factor):
        img = Image.open(image)
        try:
            contrast = ImageEnhance.Contrast(image)
            img = contrast.enhance(contrast_factor)

            # Adjust brightness
            brightness = ImageEnhance.Brightness(img)
            img = brightness.enhance(brightness_factor)

            return img
        except:
            raise Exception("Unable to adjust exposure. Check image, contrast_factor, brightness_factor")
    @staticmethod    
    def rotate_image(img, degrees, flip_horizontal=False, flip_vertical=False):
        img = Image.open(img)
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
    @staticmethod    
    def resize_image(img, width, height, width_unit='px', height_unit='px', mode='contain', aspect_ratio=None):
        img = Image.open(img)
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
    @staticmethod    
    def apply_filter(img, filter_name):
        img = Image.open(img)
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
        
    @staticmethod    
    def get_image_type(image, option):
        my_string = f"{settings.MEDIA_URL}{image.image}"
        # Find the index of the last occurrence of the period
        last_index = my_string.rfind('.')
        # Extract the substring from the last period to the end, or return an empty string if no period is found
        if option==">":
            result = my_string[last_index:] if last_index != -1 else ""
        else:    
            result = my_string[:last_index] if last_index != -1 else my_string
        return result
    @staticmethod
    def convert_image(image_path):
        try:
            # image = Image.open(image_a_path)
            prev_type = Effects.get_image_type(image_path, "<")
            # new_type = f"Media/{image_path.image}".replace(prev_type, type)
            # image.save(new_type)
            # print(new_type)
            return prev_type 
        except Exception as e:
            raise Exception(f"Error: {e}")

