# urls.py
from django.urls import path, include
from rest_framework_nested import routers
from .views import OrderViewSet

# Create a router instance
router = routers.SimpleRouter()

# Register your ViewSet with the router
router.register("orders", OrderViewSet, basename="orders")

urlpatterns = [
    path(r"", include(router.urls)),
]