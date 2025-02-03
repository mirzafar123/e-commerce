from django.urls import path , include
from .views import *

urlpatterns = [
  path('search/', search, name='search'),
  path('', store, name="store"), 
  path('<slug:category_slug>/', store, name="products_by_category"), 
  path('<slug:category_slug>/<slug:product_slug>/', product_detail, name="product_detail"),
 ] 

