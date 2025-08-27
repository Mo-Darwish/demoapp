from django.urls import path
from . import views
# from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
  path('api/v1/auth/jwt/register/' , views.RegisterView.as_view()),
  path('api/v1/auth/jwt/login/' , views.LoginView.as_view()) ,
  path('api/v1/auth/jwt/logout/' , views.LogoutView.as_view()),
  path('api/v1/auth/jwt/reset/' , views.RequestPasswordResetEmail.as_view()),
  path('api/v1/auth/jwt/password-reset/<uidb64>/<token>/',views.PasswordTokenCheckAPIView.as_view(),name='password-reset'),
  path('api/v1/auth/jwt/password-change/', views.UpdatePassword.as_view())
  # add for experimenting
  # path('api/v1/auth/jwt/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

]