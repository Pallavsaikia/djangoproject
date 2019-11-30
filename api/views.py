from django.shortcuts import render
from rest_framework.views import APIView
from api.serializers import RegisterSerializers
from rest_framework.response import Response
from rest_framework import status
from api.CustomResponse import CustomResponse


# Create your views here.
class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            # serializer.save()
            response = CustomResponse(success=True)
            return Response(response.get_response, status=status.HTTP_200_OK)
        response = CustomResponse(success=False, error=serializer.errors)
        return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)
