# sale_order/urls.py
from django.urls import path, include
from rest_framework_nested import routers
from .views import OrderViewSet, SaleOrderView, OrdersViewV2 , sale_order_ui
app_name = 'sale_order'
v1_router = routers.SimpleRouter()
v2_router = routers.SimpleRouter()

# Register ViewSets with the v1 router
v1_router.register("orders", OrderViewSet, basename="orders")
v1_router.register("sale-orders", SaleOrderView, basename="sale-orders-v1")

# Register ViewSets with the v2 router
v2_router.register("sale-orders", OrdersViewV2, basename="sale-orders-v2")

urlpatterns = [
    path("v1/", include((v1_router.urls, 'sale_order'), namespace="v1")),
    path("v2/", include((v2_router.urls, 'sale_order'), namespace="v2")),
    path('ui/', sale_order_ui, name='sale_order_ui'),

]