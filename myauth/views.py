from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model, authenticate

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from .serializers import UserSerializer

from rest_framework_jwt.utils import jwt_payload_handler, jwt
from django.conf import settings
from django.contrib.auth.signals import user_logged_in


User = get_user_model()

class CreateUserAPIView(APIView):
    def get(self, request):
        return HttpResponseForbidden()
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)

    def create_data(self, obj, errors=0):
        data = obj
        data['errors'] = errors
        return data

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(self.create_data({'user': serializer.data}), status=status.HTTP_201_CREATED) # ???????

        return Response(self.create_data(serializer.errors, len(serializer.errors)), status=status.HTTP_400_BAD_REQUEST)
    

class UserAuth(APIView):
    def get(self, request):
        return HttpResponseForbidden()
    
    permission_classes = (AllowAny,)
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        try:
            user = User.objects.get(username=username) # authenticate(email=email, password=password)
            if user.check_password(password):
                if not user.is_active:
                    res = {'login_status': 3, 'message': 'user banned'}
                    return Response(res, status=status.HTTP_403_FORBIDDEN)
                
                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                
                payload = jwt_payload_handler(user)
                token = jwt.encode(payload, settings.SECRET_KEY)
                res = {'login_status': 1, 'message': 'success auth'}
                res['token'] = token
                res['user'] = {
                    'user_id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'age': user.age,
                    'is_active': user.is_active,
                    'is_staff': user.is_staff,
                    'data_joined': user.date_joined
                }
                return Response(res, status=status.HTTP_200_OK)
            else:
                res = {'login_status': 2, 'message': 'wrong password'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)

        except User.DoesNotExist:
            res = {'login_status': 4, 'message': 'user does not exist'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
