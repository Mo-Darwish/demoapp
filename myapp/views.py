from rest_framework import generics, status
from rest_framework.views import  APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
# Create your views here.
from drf_yasg.utils import swagger_auto_schema

import logging

logger = logging.getLogger("django.request")
class Home(APIView):
    authentication_classes = [JWTAuthentication]
    @swagger_auto_schema(
        security=[{'Bearer': []}]
    )
    def get(self, request):
        if request.user.is_authenticated:
            content = {'message': 'Hello, World!'}
            return Response(content)
        else :
            logger.critical("Platform is running at risk")
            logger.info("MyView GET called by user %s", request.user)
            return Response(status=status.HTTP_400_BAD_REQUEST)

class UserView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    def get_object(self):
        return self.request.user