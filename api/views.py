from django.shortcuts import render
from rest_framework.views import APIView
from api.serializers import RegisterSerializers, LoginSerializers
from rest_framework.response import Response
from rest_framework import status
from api.CustomResponse import CustomResponse
from django.contrib.auth.models import auth
from first_project.settings import TOKEN_KEY
import jwt


# Create your views here.
class RegisterApiView(APIView):
    def post(self, request):
        serializer = RegisterSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            response = CustomResponse(success=True)
            return Response(response.get_response, status=status.HTTP_200_OK)
        response = CustomResponse(success=False, error=serializer.errors)
        return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):

    def post(self, request):
        serializer = LoginSerializers(data=request.data)
        if serializer.is_valid():
            username = serializer.data['username']
            password = serializer.data['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None and not user.is_staff:
                token = jwt.encode({"username": username}, TOKEN_KEY, algorithm="HS256")
                response = CustomResponse(success=True, data={"token": token})
                return Response(response.get_response, status=status.HTTP_200_OK)
            else:
                response = CustomResponse(success=False, error={"error": "Username or password not valid"})
                return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)
        response = CustomResponse(success=False, error=serializer.errors)
        return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)


class AskQueryApiView(APIView):
    def post(self, request):
        token = request.META['HTTP_AUTHORIZATION']
        check=str(request.token_decode)
        print(check)
        print(check)
        print(check)
        print(check)
        print(check)
        try:
            decode = jwt.decode(token, TOKEN_KEY, algorithms=["HS256"])
        except:
            response = CustomResponse(success=False, error={"invalid token": "token"})
            return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)
        return Response(decode, status=status.HTTP_200_OK)