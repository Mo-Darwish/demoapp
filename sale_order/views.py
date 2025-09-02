from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .services import OrderService
from .serializers import OrderDetailSerializer

class OrderViewSet(viewsets.GenericViewSet):
    serializer_class = OrderDetailSerializer

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

        serializer = self.get_serializer(queryset.first())
        return Response(serializer.data)