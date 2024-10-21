from django.db import models
from CustomUser.models import Customuser
from .cloudinary import upload_to_cloudinary

# Create your models here.
class HandleImageCreation(models.Manager):
    def create_image(self, user, name, image):
        if not image:
            raise ValueError("Input Image is required")
        
        uploaded_image_data = upload_to_cloudinary(image)
        user_image = self.model(user=user)
        user_image.name = name
        user_image.image = uploaded_image_data["secure_url"]
        user_image.public_id = uploaded_image_data["public_id"]
        user_image.save()
        return user_image

# Model to store user images
class UserImages(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE, related_name="loggedin_user_image")
    name = models.CharField(max_length=100)
    image = models.URLField(blank=True)
    public_id = models.CharField(max_length=1000, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = HandleImageCreation()  # Use the custom manager

    def __str__(self):
        return f"Image by {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"