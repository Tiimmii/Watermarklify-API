from datetime import datetime
from cloudinary.uploader import upload, destroy
from django.conf import settings
from gateway.authentication import get_random

def upload_to_cloudinary(image, old_public_id=None):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    cloudinary_folder_name = settings.CLOUDINARY_FOLDER_PATH
    file_name = f"{timestamp}_{get_random(10)}"
    public_id = f"{cloudinary_folder_name}/{file_name}"

    if old_public_id:
        try:
            destroy(old_public_id)  # Delete the previous image
        except Exception as e:
            print(f"Error deleting old image: {e}")

    # Upload the new image to Cloudinary
    uploaded_image = upload(image, public_id=public_id, overwrite=True)
    uploaded_image_url = uploaded_image["secure_url"]
    uploaded_public_id = uploaded_image["public_id"]

    return  [uploaded_image_url, uploaded_public_id]
        
    
