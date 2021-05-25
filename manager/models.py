from django.db import models


# Create your models here.
class Item(models.Model):
    name = models.CharField(max_length=100)
    stock = models.PositiveIntegerField(default=0)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    purchasing_price = models.DecimalField(max_digits=12, decimal_places=2)
    note = models.TextField
    category = models.CharField(max_length=20,default=None, blank=True, null=True)

    def __str__(self):
        return str(self.name) + " | " + str(self.stock) + " | " + str(self.unit_price)+"/"+str(self.purchasing_price)
