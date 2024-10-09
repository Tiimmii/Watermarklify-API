from django.db import models
from CustomUser.models import Customuser

# Create your models here.
class UserImages(models.Model):
    user = models.ForeignKey(Customuser, on_delete=models.CASCADE, related_name="loggedin_user_image")
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="WATERMARKLIFY_IMAGES/", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Image by {self.user.username} - {self.created_at.strftime('%Y-%m-%d')}"