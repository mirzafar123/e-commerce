from django.db import models
from store.models import Product , Variation



# Create your models here.
class Cart(models.Model):
    date_added = models.DateTimeField(auto_now_add=True)
    session_id = models.CharField(max_length=200, default='')


class CartItem(models.Model):
    def get_total_price(self):
        return self.quantity * self.product.price
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)
    variations = models.ManyToManyField(Variation, blank=True)

    def __str__(self):
        return str(self.product)