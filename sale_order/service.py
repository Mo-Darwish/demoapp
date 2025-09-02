from .models import Orders_details
from django.db.models import Sum

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

