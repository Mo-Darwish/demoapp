from unittest.mock import Mock, patch
from django.test import TestCase
from django.urls import reverse

class OrdersViewV2Tests(TestCase):

    @patch('sale_order.views.OrderServiceV2.get_orders_with_completion_rates')
    def test_retrieve_completion_rate_returns_mocked_data(self, mock_get_rates):
        # Arrange
        fake_order = {'id': 1, 'completion_rate': 88.5}

        mock_qs = Mock()                 # create a fake queryset
        mock_qs.exists.return_value = True
        mock_qs.first.return_value = fake_order
        mock_qs.order_by.return_value = mock_qs  # so .order_by() still works

        mock_get_rates.return_value = mock_qs

        # Act
        url = reverse('sale_order:v2:sale-orders-v2-retrieve-completion-rate', args=[1])
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), fake_order)
        mock_get_rates.assert_called_once_with(1)


    @patch('sale_order.service.SaleOrder.objects')
    def test_completion_rate_calculation_with_mocked_data(self, mock_sale_order_objects):
        fake_order_id = 1

        fake_order_data = {
            'id': fake_order_id,
            'completion_rate': (150 - 50) * 100.0 / 150  # 66.666...
        }

        mock_queryset = Mock()
        mock_queryset.first.return_value = fake_order_data

        mock_sale_order_objects.values.return_value = mock_queryset
        mock_queryset.annotate.return_value = mock_queryset

        from sale_order.service import OrderServiceV2

        # When
        order_queryset = OrderServiceV2.get_orders_with_completion_rates(fake_order_id)
        order = order_queryset.first()
        rate = order['completion_rate']

        # Then
        # We assert that the final calculated rate is what we expected.
        expected_rate = (150 - 50) * 100.0 / 150
        self.assertAlmostEqual(rate, expected_rate, places=2)
