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

def create_token(object_model):
    payload = jwt_payload_handler(object_model)
    return jwt.encode(payload, settings.SECRET_KEY)

class CreateUserAPIView(APIView):
    def get(self, request):
        return HttpResponseForbidden()
    # Allow any user (authenticated or not) to access this url
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def create_data(self, obj, errors=0):
        data = obj
        data['errors'] = errors
        return data

    def post(self, request):
        data = {  # getting form fields data
            'username': request.data.get('login'),
            'email': request.data.get('email'),
            'password': request.data.get('password'),
            'first_name': request.data.get('first_name', ''),
            'last_name': request.data.get('last_name', ''),
            'age': request.data.get('age')
        }
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(self.create_data({'user': serializer.data}), status=status.HTTP_201_CREATED) # ???????

        return Response(self.create_data(serializer.errors, len(serializer.errors)), status=status.HTTP_400_BAD_REQUEST)
    

class UserAuth(APIView):
    def get(self, request):
        return HttpResponseForbidden()
    
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('login')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username) # authenticate(email=email, password=password)
            if user.check_password(password):
                if not user.is_active:
                    res = {'login_status': 3, 'message': 'user banned'}
                    return Response(res, status=status.HTTP_403_FORBIDDEN)
                
                serializer = self.serializer_class(instance=user)

                user_logged_in.send(sender=user.__class__,
                                    request=request, user=user)
                token = create_token(user)
                
                res = {'login_status': 1, 'message': 'success auth'}
                res['token'] = token
                res['user'] = serializer.data
                return Response(res, status=status.HTTP_200_OK)
            else:
                res = {'login_status': 2, 'message': 'wrong password'}
                return Response(res, status=status.HTTP_403_FORBIDDEN)

        except User.DoesNotExist:
            res = {'login_status': 4, 'message': 'user does not exist'}
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

class GetUserInfo(APIView):
    def get(self, request):
        return HttpResponseForbidden
    
    # default permission_classes
    serializer_class = UserSerializer
    def post(self, request):
        print(request.user)
        if request.data.get('online'):
            user_logged_in.send(sender=request.user.__class__,
                                    request=request, user=request.user)
        serializer = self.serializer_class(instance=request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

class RefreshToken(APIView):
    def get(self, request):
        return HttpResponseForbidden
    
    # default permission_classes
    def post(self, request):
        token = create_token(request.user)
        return Response({'token': token}, status=status.HTTP_200_OK)