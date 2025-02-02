from django.urls import path 
from .views import *

from adana.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static

urlpatterns = [
    path('', cart, name="cart"),
    path('add_product/<int:product_id>/', add_cart, name="cart_add"),
    path('sub_product/<int:product_id>/', sub_cart, name="cart_sub"),
    path('remove_product/<int:product_id>/', sub_cart, name="remove_product")
]