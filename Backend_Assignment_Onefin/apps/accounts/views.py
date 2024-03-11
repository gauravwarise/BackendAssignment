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
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.db.models import Q
# Create your views here.

class UserRegistrationView(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        try:
            data = request.data
            context = dict()
            serializer = UserSerializer(data=data)

            if serializer.is_valid():
                password = make_password(data.get('password'))
                serializer.validated_data['password'] = password

                serializer.save()
                user = authenticate(username=request.data["username"], password=request.data["password"])

                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                context['access_token'] = access_token
                

                resp = JsonResponse(context, status=context.get(
                            'httpstatus', HTTP_201_CREATED))
                resp.set_cookie('access_token', access_token)
                return resp
            else:
                context["status"] =   "error"
                context["message"] = "Registration Failed!!!"
                context["http_status"] = HTTP_400_BAD_REQUEST

        except Exception as e:
            context["status"] = "error"
            context["message"] = "Registration Failed!!!"
            context["http_status"] = HTTP_400_BAD_REQUEST

        return JsonResponse(context, status=context.get('http_status', HTTP_200_OK))

