from django.urls import path
from .views import Home , UserView

urlpatterns = [
    path('home', Home.as_view()),
    path('users/' , UserView.as_view()),
]