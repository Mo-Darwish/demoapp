from django.contrib.auth import authenticate

from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import LogoutSerializer, UserRegistrationSerializer, LogInSerializer , ResetPasswordViaEmailSerializer, UpdatePasswordSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
# ---
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core import serializers
# Imports for drf-yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

class RegisterView(APIView):
    authentication_classes = []
    throttle_scope = 'register'
    @swagger_auto_schema(request_body=UserRegistrationSerializer)
    def post(self, request):
        if   request.version  != "v1" :
            return Response({"message": f"API Version: {request.version}"} , status=status.HTTP_400_BAD_REQUEST)
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data , status=status.HTTP_201_CREATED)


class LoginView(APIView) :
  authentication_class = []
  @swagger_auto_schema(request_body=LogInSerializer)
  def post(self, request) :
    if   request.version  != "v1" :
        return Response({"message": f"API Version: {request.version}, it should be v1"} , status=status.HTTP_400_BAD_REQUEST)
    serializer = LogInSerializer(data = request.data , context={'request': request})
    serializer.is_valid(raise_exception = True)
    # print("the data from serializer : " , serializer.data)
    user = authenticate(request , username = serializer.data['username'] , password = serializer.data['password'])
    if user is  None :
            raise serializer.ValidationError({"status": "error", "message": "Username or password doesn't match. Please try again."})

    if not user.is_active:
            raise serializer.ValidationError({"status": "error", "message": "Account not verified."})

    token = get_tokens_for_user(user)
    return Response(token , status=status.HTTP_201_CREATED)


class LogoutView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['refresh_token'],
            properties={
                'refresh_token': openapi.Schema(type=openapi.TYPE_STRING, description="The refresh token to be blacklisted.")
            },
        )
    )
    def post(self, request):
        # Use the serializer to validate the request data
        serializer = LogoutSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=status.HTTP_205_RESET_CONTENT)

# ---- password reset

class PasswordTokenCheckAPIView(APIView):
    serializer_class = UpdatePasswordSerializer
    @swagger_auto_schema(request_body=UpdatePasswordSerializer)

    def patch(self, request, uidb64,token):
            id= smart_str(urlsafe_base64_decode(uidb64))
            user= User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                return Response({'error':'token is not valid, please check the new one'},status=status.HTTP_401_UNAUTHORIZED)
            serializer = self.serializer_class(request.user , data = request.data)
            serializer.is_valid(raise_exception = True)
            serializer.save()
            return Response({'sucess':True, 'message':'Password is reset successfully'},status=status.HTTP_200_OK)

class UpdatePassword(APIView):
    authentication_class = [IsAuthenticated]
    serializer_class = UpdatePasswordSerializer
    @swagger_auto_schema(
        request_body=UpdatePasswordSerializer,
        security=[{'Bearer': []}]
    )
    def patch(self , request) :
      serializer = self.serializer_class(request.user , data = request.data)
      serializer.is_valid(raise_exception = True)
      serializer.save()
      return Response({'sucess':True, 'message':'Password is changed successfully'},status=status.HTTP_200_OK)
class RequestPasswordResetEmail(APIView):
    serializer_class=ResetPasswordViaEmailSerializer
    @swagger_auto_schema(request_body=ResetPasswordViaEmailSerializer)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.data['email']

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(smart_bytes(user.id) )
            token = PasswordResetTokenGenerator().make_token(user)

            current_site=get_current_site(request=request).domain
            realtivelink = reverse('v1:password-reset',kwargs={'uidb64':uidb64,'token':token})

            absurl='http://'+current_site+realtivelink
            # absurl='http://'+''

            email_body='Hi, \nUse link below to reset your password \n' + absurl
            send_mail('reset your password' , email_body , "from@example.com" , [user.email])
        return Response({'successfully':'check your email to reset your password'},status=status.HTTP_200_OK)

# JWT

def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }



