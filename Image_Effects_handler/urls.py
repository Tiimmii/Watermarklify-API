from django.urls import path
from .views import Image_Effects

urlpatterns = [
    path('image-effects/', Image_Effects.as_view())
]