from django.urls import path 
from .views import *

from adana.settings import MEDIA_ROOT, MEDIA_URL
from django.conf.urls.static import static

urlpatterns = [
    path('', cart, name="cart"),
]