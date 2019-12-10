from rest_framework.views import APIView
from api.serializers import (
    RegisterSerializers,
    LoginSerializers,
    QuerySerializers,
    AnswerSerializers,
    QuestionSerializer,
    IntSerializer
)
from rest_framework.response import Response
from rest_framework import status
from helper.CustomResponse import CustomResponse
from django.contrib.auth.models import User
from django.contrib.auth.models import auth
from first_project.settings import PAGE_SIZE
from dashboard_app.models import Appointment
from helper.JWTDecode import JwtDecode
from helper.check_token import check_token
from django.utils.decorators import method_decorator
from dashboard_app.models import Query, Answer
import jwt
from datetime import datetime
from django.core.paginator import Paginator


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
                token = JwtDecode.encode(username=username)
                response = CustomResponse(success=True, data={"token": token})
                return Response(response.get_response, status=status.HTTP_200_OK)
            else:
                response = CustomResponse(success=False, error={"error": "Username or password not valid"})
                return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)
        response = CustomResponse(success=False, error=serializer.errors)
        return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)


class AnswerAQueryApiView(APIView):
    @method_decorator(check_token)
    def post(self, request):
        username = request.token_decode.get("username")
        user = User.objects.get(username=username)
        serializer = AnswerSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            replied_to = serializer.data['replied_to']
            query = Query.objects.get(id=replied_to)
            query.replied = False
            query.save()
            response = Response(CustomResponse(success=True).get_response, status=status.HTTP_200_OK)
            response['HTTP_AUTHORIZATION'] = JwtDecode.encode(username)
            return response
        else:
            response = CustomResponse(success=False, error=serializer.errors)
            return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)


class AskAppointmentApiView(APIView):
    @method_decorator(check_token)
    def post(self, request):
        decode = JwtDecode.decode(request)
        username = decode.get("username")
        user = User.objects.get(username=username)
        user_appointment = Appointment.objects.filter(user=user)

        appointment_count_false = user_appointment.filter(appointed=False).count()
        appointment_count_true = user_appointment.filter(appointed=True).count()
        if appointment_count_false > 0:
            response = CustomResponse(success=False, error={"appointment": "Already has one appointment request"})
            return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            if appointment_count_true == 0:
                appointment = Appointment(user=user)
                appointment.save()
                response = Response(CustomResponse(success=True).get_response, status=status.HTTP_200_OK)
                response['HTTP_AUTHORIZATION'] = JwtDecode.encode(username)
                return response
            else:
                appointment_date_passed_count = Appointment.objects.filter(user=user).filter(appointed=True).filter(
                    day_of_appointment__gte=datetime.now()).count()
                if appointment_date_passed_count == 0:
                    appointment = Appointment(user=user)
                    appointment.save()
                    response = Response(CustomResponse(success=True).get_response, status=status.HTTP_200_OK)
                    response['HTTP_AUTHORIZATION'] = JwtDecode.encode(username)
                    return response
                else:
                    response = CustomResponse(success=False,
                                              error={"appointment": "Already has one appointment"})
                    return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)


class QuestionApiView(APIView):
    @method_decorator(check_token)
    def post(self, request):
        username = request.token_decode.get("username")
        user = User.objects.get(username=username)
        serializer = QuerySerializers(data=request.data)
        if serializer.is_valid():
            serializer.save(user)

            response = Response(CustomResponse(success=True).get_response, status=status.HTTP_200_OK)
            response['HTTP_AUTHORIZATION'] = JwtDecode.encode(username)
            return response
        else:
            response = CustomResponse(success=False, error=serializer.errors)
            return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)

    @method_decorator(check_token)
    def get(self, request):
        username = request.token_decode.get("username")
        serializer = IntSerializer(data=request.data)

        if serializer.is_valid():
            page_num = serializer.data['page_no']
            user = User.objects.get(username=username)
            objects=None
            try:
                replied = request.data['replied']
                # print(Re)
                objects = Query.objects.filter(asked_by=user).filter(replied=replied)
            except:
                objects = Query.objects.filter(asked_by=user)
            finally:
                queryset = Paginator(objects, PAGE_SIZE)
                last_page = queryset.page_range[-1]
                if last_page >= page_num:
                    serializer = QuestionSerializer(queryset.page(page_num).object_list, many=True)
                    response = Response(
                        CustomResponse(success=True, data=serializer.data, last_page=last_page).get_response,
                        status=status.HTTP_200_OK)
                    response['HTTP_AUTHORIZATION'] = JwtDecode.encode(username)
                    return response
                else:
                    response = CustomResponse(success=False, error={"page_no": "invalid page number"})
                    return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            response = CustomResponse(success=False, error=serializer.errors)
            return Response(response.get_response, status=status.HTTP_400_BAD_REQUEST)
