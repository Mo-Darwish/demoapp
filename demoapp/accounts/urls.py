from django.urls import path
from . import views
# from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
  path('' , views.home_view , name = 'home'),
  path('api/v1/auth/login/' , views.login_view , name = 'login'),
  path('api/v1/auth/register/' , views.register_view , name ='register'),
  path('api/v1/auth/logout/' , views.logout_view , name ='logout'),
  path('api/v1/auth/reset_password/', views.reset_password_view , name = 'reset_password'),
  path('api/v1/auth/jwt/register/' , views.RegisterView.as_view()),
  path('api/v1/auth/jwt/login/' , views.LoginView.as_view()) ,
  path('api/v1/auth/jwt/logout/' , views.LogoutView.as_view()),
  # add for experimenting
  # path('api/v1/auth/jwt/logout/', TokenBlacklistView.as_view(), name='token_blacklist'),

]