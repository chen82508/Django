from .views import RegisterView, VerifyEmail
from django.urls import path, re_path

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('email-verify/', VerifyEmail.as_view(), name='email-verify'),
]