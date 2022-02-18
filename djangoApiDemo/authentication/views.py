from .models import User
from .serializers import RegisterSerializers
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.urls import reverse
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializers

    def post(self, request):
        user = request.data
        serializers = self.serializer_class(data=user)
        serializers.is_valid(raise_exception=True)
        serializers.save()

        user_data = serializers.data

        user = User.objects.get(email=user_data['email'])
        token = RefreshToken.for_user(user).access_token
        current_site = get_current_site(request).domain
        relativeLink = reverse('email-verify')
        absurl = f"http://{current_site}{relativeLink}?token={token}"
        email_body = f"Hi {user.username}! Please use the following link to verify your email.\n{absurl}"
        data = {
            "to_email": user.email,
            "email_subject": "Verify your email",
            "email_body": email_body,
        }

        Util.send_email(data)
        return Response(user_data, status=status.HTTP_201_CREATED)

class VerifyEmail(generics.GenericAPIView):
    def get(self):
        pass