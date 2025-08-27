from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.views import APIView
from accounts.serializers import UserRegistrationSerializer, LogInSerializer
from .forms import RegisterForm , ResetPasswordForm
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework import status


class RegisterView(APIView):
    authentication_classes = []
    throttle_scope = 'register'
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data , status=status.HTTP_201_CREATED)


class LoginView(APIView) :
  authentication_class = []
  def post(self, request) :
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



# -------- OLD ___________

# JWT

def get_tokens_for_user(user):
    if not user.is_active:
      raise AuthenticationFailed("User is not active")

    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }
# Create your views here.
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = User.objects.create_user(username=username, password=password)
            # JWT - token = get_tokens_for_user(user)
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form':form})

def login_view(request) :
  error = None
  if request.method == "POST" :
    username = request.POST.get("username")
    password = request.POST.get("password")
    user = authenticate(request , username = username , password = password)
    if user is not None :
      login(request, user)
      next_url = 'home'
      return redirect(next_url)
    else:
      error = "Invalid credentials"
  return render(request , 'accounts/login.html' , {'error': error})

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('login')
    else:
        return redirect('home')

def reset_password_view(request):
  error = None
  if request.method == "POST" :
    # send an email to reset the password
    form = ResetPasswordForm(request.POST)
    if form.is_valid() :
      email = form.cleaned_data.get("email")
      password = form.cleaned_data.get("password")
      user = User.objects.get(email=email)
      user.set_password(password)
      user.save()
      update_session_auth_hash(request, user)
      return redirect('login')

  else :
      form = ResetPasswordForm()
  return render(request , 'accounts/reset_password.html' , {'form':form , 'error' : error} )



# @login_required
def home_view(request) :
  return render(request , 'accounts/home.html')