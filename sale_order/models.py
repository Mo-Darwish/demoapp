from django.db import models

# Create your models here.
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





