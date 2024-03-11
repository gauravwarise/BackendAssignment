from django.shortcuts import render
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from apps.accounts.serializers import *
from django.http import JsonResponse
from rest_framework.status import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate, login, logout
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Q
# from .movie_list import getMoviesList
# Create your views here.

class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        try:
            data = request.data
            response = {"status": "success", "data": "","access_token":"", "message":"", "http_status": HTTP_201_CREATED}
            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                password = make_password(data.get('password'))
                serializer.validated_data['password'] = password

                serializer.save()
                user = authenticate(username=request.data["username"], password=request.data["password"])

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                response['access_token'] = access_token
                
                response['status'] = "success"
                response['data'] = serializer.data
                response["message"] = "Registration Seccessfully!!!"

                resp = JsonResponse(response, status=response.get(
                            'httpstatus', HTTP_201_CREATED))
                resp.set_cookie('access_token', access_token)

                return resp
            else:
                response["status"] =   "error"
                response["message"] = "Registration Failed!!!"
                response["http_status"] = HTTP_400_BAD_REQUEST
                response["data"] = serializer.errors

        except Exception as e:
            response["status"] = "error"
            response["message"] = "Registration Failed!!!"
            response["http_status"] = HTTP_400_BAD_REQUEST
            response["data"] = str(e)

        return JsonResponse(response, status=response.get('http_status', HTTP_200_OK))


class LoginUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user = authenticate(
            username=request.data["username"], password=request.data["password"]
        )  # authenticate user
        print("user ===============>", user)
        if user is not None:
            token = RefreshToken.for_user(
                user
            )  # for authenticated user jwt token is created
            # refresh_token = str(token)
            access_token = str(token.access_token)
            return Response(
                {"access_token": access_token}, status=status.HTTP_201_CREATED
            )
        return Response(
            {"message": "User authentication failed"},
            status=status.HTTP_400_BAD_REQUEST,
        )
