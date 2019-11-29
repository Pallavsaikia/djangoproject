from django.shortcuts import render
from rest_framework.views import APIView
from api.serializers import RegisterSerializers
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User


# Create your views here.
class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
