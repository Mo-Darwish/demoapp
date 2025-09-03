from .models import Orders_details , SaleOrder , ItemSaleOrder , StockExchange
from django.db.models import Sum, Case, When, F, FloatField
from django.db.models.functions import Coalesce , Round


class OrderService:
    @staticmethod
    def get_completion_rate(sale_order_id: int) -> float:
        total_quantity = (
            Orders_details.objects.filter(sale_order_id=sale_order_id)
            .aggregate(
                total_quantity=Sum('order_quantity'),
                total_stockexchange=Sum('stockexchange_quantity')
            )
        )

        total_quantity = total_quantity['total_quantity']
        total_stockexchange = total_quantity['total_stockexchange'] or 0

        completion_rate = (total_quantity - total_stockexchange) / total_quantity * 100
        return completion_rate


    @staticmethod
    def get_orders_with_completion_rates(sale_order_id=None):
        """
        Get orders with completion rates - either single order or all orders
        """
        queryset = (
            Orders_details.objects
            .values('sale_order_id')
            .annotate(
                total_quantity=Sum('order_quantity'),
                total_stockexchange=Coalesce(Sum('stockexchange_quantity'),0)
            )
            .annotate(
                completion_rate= Round(Case(
                    When(total_quantity__gt=0,
                         then=(F('total_quantity') - F('total_stockexchange')) * 100.0 / F('total_quantity')),
                    default=0.0,
                    output_field=FloatField()
                ) , precision= 2)
            )
        )

        if sale_order_id:
            queryset = queryset.filter(sale_order_id=sale_order_id)

        return queryset


class SaleOrderService :
    @staticmethod
    def create_sale_order(status : str) -> SaleOrder :
        return SaleOrder.objects.create(status = status)

    # def create_item_sale_order(* , status)



