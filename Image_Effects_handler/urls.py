from django.urls import path
from .views import Image_Effects, Handle_Image_Effects

urlpatterns = [
    path('image-effects', Image_Effects.as_view()),
    path('image-effects/<int:pk>', Handle_Image_Effects.as_view()),
]