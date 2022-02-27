from .models import User
from .renderers import UserRenderer
from .serializers import (
    EmailVerificationSerializer, LoginSerializer, RegisterSerializer, ResetPasswordEmailRequestSerializer, SetNewPasswordSerializer)
from .utils import Util
from django.conf import settings
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render
from django.urls import reverse
from django.utils.encoding import (
    smart_str, force_str, smart_bytes, DjangoUnicodeDecodeError)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import (generics, status, views)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
import jwt


# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    renderer_classes = (UserRenderer,)

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data

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


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    token_param_config = openapi.Parameter(
        'token', in_=openapi.IN_QUERY, description='Decription', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response({"email": "Successfully activated."}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({"error": "Activation expired."}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError:
            return Response({"error": "Invalid token."}, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        email = request.data['email']
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            relativeLink = reverse(
                'password-reset-confirm', kwargs={'uidb64': uidb64, 'token': token})
            absurl = f"http://{current_site}{relativeLink}"
            email_body = f"Hello,\n please use the following link to reset your passwrod.\n{absurl}"
            data = {
                "to_email": user.email,
                "email_subject": "Reset your password",
                "email_body": email_body,
            }
            Util.send_email(data)
        return Response({"success": "We have sent you a link to reset your password."}, status=status.HTTP_200_OK)


class PasswordTokenCheckAPI(generics.GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({"error": "Token is not valid, please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)

            return Response({
                "success": True,
                "message": "Credentials valid.",
                "uidb64": uidb64,
                "token": token
            }, status=status.HTTP_200_OK)
        except DjangoUnicodeDecodeError as identifier:
            return Response({"error": "Token is not valid, please request a new one."}, status=status.HTTP_401_UNAUTHORIZED)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({"success": True, "message": "Password has been reset successfully."}, status=status.HTTP_200_OK)
