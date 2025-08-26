from django.urls import path
from .views import Home , UserView

urlpatterns = [
    path('', Home.as_view()),
    path('users/' , UserView.as_view()),
]