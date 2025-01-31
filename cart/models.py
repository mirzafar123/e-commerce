from django.db import models
from store.models import Product


# Create your models here.
class Cart(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return self.product