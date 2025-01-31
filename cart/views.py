from django.shortcuts import render

# Create your views here.

from django.shortcuts import render

def cart(request):
    return render(request, 'cart.html')