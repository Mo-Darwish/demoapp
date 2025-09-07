from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.versioning import URLPathVersioning
from .service import OrderService, SaleOrderService, OrderServiceV2
from .serializers import (
    ItemSaleOrderReadSerializer,
    OrderDetailSerializer,
    InputSaleOrderSerializer,
    InputItemSaleOrderSerializer,
    InputStockExchangeSerializer,
    OrderDetailSerializerV2,
    SaleOrderReadSerializer,
    StockExchangeReadSerializer,
    DeleteSaleOrderSerializer,
    DeleteItemSaleOrderSerializer,
    DeleteStockExchangeSaleOrderSerializer,
    UpdateItemSaleOrderSerializer,
    UpdateStockExchangeSerializer,
)
# Imports for drf-yasg
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import SaleOrder, ItemSaleOrder, StockExchange
from django.shortcuts import render, get_object_or_404

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

class OrdersViewV2(viewsets.GenericViewSet) :
    serializer_class = OrderDetailSerializerV2

    def get_queryset(self):
        return True

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
        queryset = OrderServiceV2.get_orders_with_completion_rates(sale_order_id)
        if not queryset.exists():
            return Response(
                {'error': f'Sale order {sale_order_id} not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = self.get_serializer(queryset.order_by('id').first())
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='completion-rates')
    def list_completion_rates(self, request):
        """Get all orders with completion rates"""
        queryset = OrderServiceV2.get_orders_with_completion_rates()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
class SaleOrderView(viewsets.GenericViewSet) :

    def get_queryset(self):
        return True
    authentication_classes = []
    serializer_class = InputSaleOrderSerializer
    serializer_class_by_action = {
        "create_sale_order" : InputSaleOrderSerializer ,
        "create_bulk_items" : InputItemSaleOrderSerializer,
        "create_bulk_stockexchange_items" : InputStockExchangeSerializer

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

    @action(detail = False , methods = ['post'])
    def create_bulk_stockexchange_items(self , request) :
        serializer = self.get_serializer(data=request.data , many = True)
        serializer.is_valid(raise_exception=True)
        SaleOrderService.create_stockexchange_sale_order(serializer.validated_data)
        return Response(serializer.data , status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='sale_orders')
    def list_sale_orders(self, request):
        queryset = SaleOrder.objects.all()
        serializer = SaleOrderReadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='bulk_items')
    def list_bulk_items(self, request):
        queryset = ItemSaleOrder.objects.all()
        serializer = ItemSaleOrderReadSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='bulk_stockexchange_items')
    def list_bulk_stockexchange_items(self, request):
        queryset = StockExchange.objects.all()
        serializer = StockExchangeReadSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=DeleteSaleOrderSerializer)
    @action(detail=False, methods=['delete'], url_path='delete_sale_order')
    def delete_sale_order(self, request):
        sale_order_id = request.data.get('sale_order_id')
        if not sale_order_id:
            return Response({'error': 'sale_order_id is required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            sale_order = SaleOrder.objects.get(id=sale_order_id)
            sale_order.soft_delete()
            return Response({'status': 'success', 'message': f'SaleOrder {sale_order_id} soft deleted.'})
        except SaleOrder.DoesNotExist:
            return Response({'error': f'SaleOrder {sale_order_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=DeleteItemSaleOrderSerializer)
    @action(detail=False, methods=['delete'], url_path='delete_item_sale_order')
    def delete_item_sale_order(self, request):
        sale_order_id = request.data.get('sale_order_id')
        brand_item_id = request.data.get('brand_item_id')
        if not sale_order_id or not brand_item_id:
            return Response({'error': 'sale_order_id and brand_item_id are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            item = ItemSaleOrder.objects.get(sale_order_id=sale_order_id, brand_item_id=brand_item_id)
            item.soft_delete()
            return Response({'status': 'success', 'message': f'ItemSaleOrder {sale_order_id}-{brand_item_id} soft deleted.'})
        except ItemSaleOrder.DoesNotExist:
            return Response({'error': f'ItemSaleOrder {sale_order_id}-{brand_item_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(request_body=DeleteStockExchangeSaleOrderSerializer)
    @action(detail=False, methods=['delete'], url_path='delete_stockexchange_sale_order')
    def delete_stockexchange_sale_order(self, request):
        sale_order_id = request.data.get('sale_order_id')
        brand_item_id = request.data.get('brand_item_id')
        if not sale_order_id or not brand_item_id:
            return Response({'error': 'sale_order_id and brand_item_id are required'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            stock = StockExchange.objects.get(sale_order_id=sale_order_id, brand_item_id=brand_item_id)
            stock.soft_delete()
            return Response({'status': 'success', 'message': f'StockExchange {sale_order_id}-{brand_item_id} soft deleted.'})
        except StockExchange.DoesNotExist:
            return Response({'error': f'StockExchange {sale_order_id}-{brand_item_id} not found.'}, status=status.HTTP_404_NOT_FOUND)

class ItemSaleOrderViewSet(viewsets.GenericViewSet):
    @swagger_auto_schema(request_body=UpdateItemSaleOrderSerializer)
    @action(detail=False, methods=['patch'], url_path='update_item_sale_order')
    def update_item_sale_order(self, request):
        serializer = UpdateItemSaleOrderSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            item = SaleOrderService.update_item_sale_order(**serializer.validated_data)
        except ItemSaleOrder.DoesNotExist:
            return Response(
                {'error': f'ItemSaleOrder {serializer.validated_data["sale_order_id"]}-'
                      f'{serializer.validated_data["brand_item_id"]} not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
        return Response({
            'status': 'success',
            'message': f'StockExchange {item.sale_order_id}-{item.brand_item_id} updated.'
        })
class StockExchangeViewSet(viewsets.GenericViewSet):
    @swagger_auto_schema(request_body=UpdateStockExchangeSerializer)
    @action(detail=False, methods=['patch'], url_path='update_stockexchange_sale_order')
    def update_stockexchange_sale_order(self, request):
        serializer = UpdateStockExchangeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            item = SaleOrderService.update_stockexchange_sale_order(**serializer.validated_data)
        except StockExchange.DoesNotExist:
            return Response(
                {'error': f'StockExchange {serializer.validated_data["sale_order_id"]}-'
                      f'{serializer.validated_data["brand_item_id"]} not found.'},
            status=status.HTTP_404_NOT_FOUND
        )
        return Response({
            'status': 'success',
            'message': f'StockExchange {item.sale_order_id}-{item.brand_item_id} updated.'
        })

def sale_order_ui(request):
    return render(request, 'sale_order.html')



