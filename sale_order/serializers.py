from .models import Orders_details
from rest_framework import serializers
class OrdersDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for user orders details.
    """
    sale_order_id = serializers.IntegerField(
        required=True,
    )
    order_quantity = serializers.IntegerField(required = True,)
    stockexchange_quantity = serializers.IntegerField()
    quantity_post_market = serializers.IntegerField()
    quantity_at_market = serializers.IntegerField()


    class Meta:
        model = Orders_details
        fields = ('sale_order_id', 'order_quantity', 'stockexchange_quantity', 'quantity_post_market', 'quantity_at_market')
    def validate(self , data ) :
      order_qty = data.get('order_quantity')
      if order_qty < 0 :
        raise serializers.ValidationError("Not A Valid Order")
      elif order_qty < (data.get('stockexchange_quantity') + data.get('quantity_at_market')) :
         raise serializers.ValidationError("Requested quantity is more than the order quantity")
      else :
        return data

class OrderDetailSerializer(serializers.Serializer):
    """
    Serializer for an Order with its completion rate.
    """
    # These fields are still populated by the .annotate() in the view
    sale_order_id = serializers.IntegerField()
    completion_rate = serializers.FloatField(read_only=True)