from django.urls import path
from .views import Loginview, Registerview, Refreshview, Getsecuredinfo, PasswordTokenCheckAPI

urlpatterns = [
    path('SignIn/', Loginview.as_view()),
    path('SignUp/', Registerview.as_view()),
    path('refresh/', Refreshview.as_view()),
    path('securedinfo/', Getsecuredinfo.as_view),
    path('password-reset/<uidb64>/token/', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
]