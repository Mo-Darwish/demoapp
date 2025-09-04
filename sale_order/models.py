from django.utils import timezone
from django.db import models

# Create your models here.

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True  # no DB table for this model

    def soft_delete(self):
        """method to soft-delete the record."""
        self.deleted_at = timezone.now()
        self.save()

    def restore(self):
        """Restore a soft-deleted record."""
        self.deleted_at = None
        self.save()
class Payments(models.Model) :
  company_branch_id = models.IntegerField()
  credit = models.DecimalField(decimal_places=2, max_digits=10 , null=True)
  debit = models.DecimalField(decimal_places=2, max_digits=10 , null=True)
  date = models.DateTimeField(null=True)
  sale_order_id = models.IntegerField(null=True)

  class Meta :
    verbose_name = "Payment"
    verbose_name_plural = "Payments"
    ordering = ['date']

class Orders(models.Model) :
  company_branch_id = models.IntegerField()
  order_id = models.IntegerField()
  order_date = models.DateTimeField()
  payment_due_date = models.DateTimeField()
  payment_amount = models.DecimalField(decimal_places=2, max_digits=10)
  installment_no = models.IntegerField()
  is_cash_like_payment = models.BooleanField()

  class Meta :
    verbose_name = "Order"
    verbose_name_plural = "Orders"
    unique_together = ['order_id', 'installment_no']

class Orders_details(models.Model) :
  sale_order_id = models.IntegerField()
  brand_item_id = models.IntegerField()
  order_quantity = models.IntegerField()
  stockexchange_quantity = models.IntegerField(null = True)
  quantity_post_market = models.IntegerField(null = True)
  quantity_at_market = models.IntegerField(null= True)

  class Meta :
    verbose_name = "Order Details"

class SaleOrder(BaseModel):
    status = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Sale Order"


class ItemSaleOrder(BaseModel):
    sale_order = models.ForeignKey(
        SaleOrder,
        on_delete=models.CASCADE,
        related_name='items'
    )
    brand_item_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        verbose_name = "Item Sale Order"
        unique_together = ('sale_order', 'brand_item_id')



class StockExchange(BaseModel):
    sale_order = models.ForeignKey(
        SaleOrder,
        on_delete=models.CASCADE,
        related_name='stock_exchanges'
    )
    brand_item_id = models.IntegerField()
    quantity = models.IntegerField()

    class Meta:
        verbose_name = "Stock Exchange"
        unique_together = ('sale_order', 'brand_item_id')








