from django.urls import path
from . import views
from django.conf import settings
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

if 'rest_framework' in settings.INSTALLED_APPS:
    from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
    urlpatterns += [
        path('api/v1/auth/jwt/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
        path('api/v1/auth/jwt/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
        path('api/v1/auth/jwt/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    ]