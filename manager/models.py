from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    purchasing_price = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField
    category = models.CharField(max_length=20, default=None, blank=True, null=True)

    def __str__(self):
        return str(self.name)


PENDING = 'PD'  # unpaid
SHIPPING = 'SP'  # paid, shipping
FINISHED = 'FN'  # paid, shipped and delivered

STATUS_CHOICES = [
    (PENDING, 'Pending'),
    (SHIPPING, 'Shipping'),
    (FINISHED, 'Finished')
]


class Order(models.Model):
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=PENDING)
    created_time = models.DateTimeField(auto_now=True)  # TODO: auto-now should be False
    description = models.CharField(max_length=500, null=True, blank=True)
    shipping_address = models.TextField(blank=True, null=True)
    buyer = models.CharField(max_length=100, default="")
    profit = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tracking_number = models.TextField(blank=True, null=True)


class OrderItems(models.Model):
    # FKs
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='orderitems', null=False)
    item = models.ForeignKey(Item, on_delete=models.PROTECT, null=False)
    # price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)

    quantity = models.IntegerField(default=1, null=False)
    offset = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)  # only applicable for one single order
