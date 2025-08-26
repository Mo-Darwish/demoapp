from django.urls import path
from . import views

urlpatterns = [
  path('' , views.home_view , name = 'home'),
  path('api/v1/auth/login/' , views.login_view , name = 'login'),
  path('api/v1/auth/register/' , views.register_view , name ='register'),
  path('api/v1/auth/logout/' , views.logout_view , name ='logout'),
  path('api/v1/auth/reset_password/', views.reset_password_view , name = 'reset_password'),
]