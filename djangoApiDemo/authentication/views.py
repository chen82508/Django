from .serializers import RegisterSerializers
from django.shortcuts import render
from rest_framework import generics, status
from rest_framework.response import Response

# Create your views here.
class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializers

    def post(self, request):
        user = request.data
        serializers = self.serializer_class(data=user)
        serializers.is_valid(raise_exception=True)
        serializers.save()

        user_data = serializers.data

        return Response(user_data, status=status.HTTP_201_CREATED)