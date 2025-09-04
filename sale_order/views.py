from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .service import OrderService, SaleOrderService
from .serializers import OrderDetailSerializer , InputSaleOrderSerializer , InputItemSaleOrderSerializer
# Imports for drf-yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
class OrderViewSet(viewsets.GenericViewSet):
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        return True

    @swagger_auto_schema(
        operation_description="Get all orders with completion rates",
        responses={
            status.HTTP_200_OK: OrderDetailSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Authentication credentials were not provided or are invalid"
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="You do not have permission to perform this action"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Order not found"
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Unexpected server error"
            ),
        }
    )
    @action(detail=False, methods=['get'], url_path='completion-rates')
    def list_completion_rates(self, request):
        """Get all orders with completion rates"""
        queryset = OrderService.get_orders_with_completion_rates()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


    @swagger_auto_schema(
        operation_description="Get all orders with completion rates",
        responses={
            status.HTTP_200_OK: OrderDetailSerializer(many=True),
            status.HTTP_400_BAD_REQUEST: openapi.Response(
                description="Bad request — invalid parameters only accept int sale order id"
            ),
            status.HTTP_401_UNAUTHORIZED: openapi.Response(
                description="Authentication credentials were not provided or are invalid"
            ),
            status.HTTP_403_FORBIDDEN: openapi.Response(
                description="You do not have permission to perform this action"
            ),
            status.HTTP_404_NOT_FOUND: openapi.Response(
                description="Orders not found"
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR: openapi.Response(
                description="Unexpected server error"
            ),
        }
    )
    @action(detail=True, methods=['get'], url_path='completion-rate')
    def retrieve_completion_rate(self, request, pk=None):
        """Get completion rate for specific order"""
        try:
            sale_order_id = int(pk)
        except ValueError:
            return Response(
                {'error': 'Invalid sale_order_id format'},
                status=status.HTTP_400_BAD_REQUEST
            )

        queryset = OrderService.get_orders_with_completion_rates(sale_order_id)

        if not queryset.exists():
            return Response(
                {'error': f'Sale order {sale_order_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(queryset.order_by('sale_order_id').first())
        return Response(serializer.data)


class SaleOrderView(viewsets.GenericViewSet) :

    def get_queryset(self):
        return True
    authentication_classes = []
    serializer_class = InputSaleOrderSerializer
    serializer_class_by_action = {
        "create_sale_order" : InputSaleOrderSerializer ,
        "create_bulk_items" : InputItemSaleOrderSerializer

    }
    def get_serializer_class(self):
        """
        Pick serializer based on the current action name.
        Defaults to `serializer_class` if not found in the dict.
        """
        return self.serializer_class_by_action[self.action]

    @swagger_auto_schema(request_body=InputSaleOrderSerializer)
    @action(detail=False, methods=['post'])
    def create_sale_order(self, request):
        if   request.version  != "v1" :
            return Response({"message": f"API Version: {request.version}"} , status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        SaleOrderService.create_sale_order(**serializer.validated_data)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

    @action(detail = False , methods = ['post'])
    def create_bulk_items(self , request) :
        serializer = self.get_serializer(data=request.data , many = True)
        serializer.is_valid(raise_exception=True)
        SaleOrderService.create_item_sale_order(serializer.validated_data)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

