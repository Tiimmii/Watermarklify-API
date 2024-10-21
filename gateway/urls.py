from django.urls import path
from .views import Loginview, Registerview, Refreshview, Getsecuredinfo, PasswordTokenCheckAPI, RequestPasswordResetEmail, SetNewPassword, VerifyEmail

urlpatterns = [
    path('SignIn', Loginview.as_view()),
    path('SignUp', Registerview.as_view()),
    path('refresh', Refreshview.as_view()),
    path('securedinfo', Getsecuredinfo.as_view),
    path('email-verify', VerifyEmail.as_view(), name="email-verify"),
    path('request-reset-email', RequestPasswordResetEmail.as_view(), name = 'request-reset-email'),
    path('password-reset/<uidb64>/<token>', PasswordTokenCheckAPI.as_view(), name='password-reset-confirm'),
    path('password-reset-complete', SetNewPassword.as_view(), name='password-reset-complete')
]