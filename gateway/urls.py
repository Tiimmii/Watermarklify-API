from django.urls import path
from .views import Loginview, Registerview, Refreshview, Getsecuredinfo

urlpatterns = [
    path('SignIn/', Loginview.as_view()),
    path('SignUp/', Registerview.as_view()),
    path('refresh/', Refreshview.as_view()),
    path('securedinfo/', Getsecuredinfo.as_view()),
]