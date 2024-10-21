from datetime import datetime
from cloudinary import uploader 
from django.conf import settings
from gateway.authentication import get_random

def upload_to_cloudinary(image):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    cloudinary_folder_name = settings.CLOUDINARY_FOLDER_PATH
    file_name = f"{timestamp}_{get_random(10)}"
    public_id = f"{cloudinary_folder_name}/{file_name}"

    uploaded_image = uploader.upload(image, public_id=public_id, ovewrite=True)
    uploaded_image = uploaded_image["secure_url"]
    return uploaded_image
