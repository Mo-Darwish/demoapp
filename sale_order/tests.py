from django.test import TestCase
from .models import ItemSaleOrder, StockExchange, SaleOrder
from .service import OrderServiceV2  # adjust import path

class CompletionRateTests(TestCase):
    def setUp(self):
        self.so1 = SaleOrder.objects.create(status='pending')
        self.so2 = SaleOrder.objects.create(status='pending')

    def test_completion_rate_with_full_data(self):
        # Given
        ItemSaleOrder.objects.create(sale_order=self.so1, brand_item_id=1, quantity=100)
        ItemSaleOrder.objects.create(sale_order=self.so1, brand_item_id=2, quantity=50)

        StockExchange.objects.create(sale_order=self.so1, brand_item_id=1, quantity=30)
        StockExchange.objects.create(sale_order=self.so1, brand_item_id=2, quantity=20)
        # When
        order = OrderServiceV2.get_orders_with_completion_rates(self.so1.id).first()
        rate = order['completion_rate']

        # Then
        expected_rate = (150 - 50) * 100.0 / 150  # 66.666...
        self.assertAlmostEqual(rate, expected_rate, places=2)

    def test_completion_rate_with_zero_total_quantity(self):
        # Given: No items at all, only stock exchange
        StockExchange.objects.create(sale_order=self.so1, brand_item_id=1, quantity=10)

        # When
        order = OrderServiceV2.get_orders_with_completion_rates(self.so1.id).first()
        rate = order['completion_rate']

        # Then: total_quantity = 0 → completion_rate should default to 0.0
        self.assertEqual(rate, 0.0)
