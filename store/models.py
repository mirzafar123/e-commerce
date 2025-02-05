from django.db import models

# Create your models here.

from django.db import models
from django.urls import reverse
from category.models import Category


# Create your models here.
CATEGORY_CHOICES = (
    ("Color", "Color"),
    ("Size", "Size"),
    ("Material", "Material"),
)

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=500, blank=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to = 'photoes/products')
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name  
    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
class VariationManager(models.Manager):
  
  def all_types(self):
    manager= super(VariationManager, self)
    types =[i[0] for i in manager.values_list('category').distinct()]
     
    result = {}
    for category_name in types:
      result[category_name] = manager.filter(category=category_name, is_active=True)
     
    return result

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = VariationManager()


    def __str__(self) -> str:
        return f"{self.product.name} {self.category} {self.value}"