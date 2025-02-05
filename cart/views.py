from django.shortcuts import render, redirect , get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from .models import *
from django.db.models import Count


def cart(request):
    try:
        total =  tax= gen_total= quantity = 0
        cart_items = None
        cart = Cart.objects.get(session_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
        tax = (total * 2)/100
        gen_total = total + tax
    except ObjectDoesNotExist:
        pass
    
    context = {
       'cart_items': cart_items,
       'total': total,
       'quantity': quantity,
       'tax': tax,
       'gen_total': gen_total
    }
    return render(request, 'cart.html', context)


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):       
    
    product = Product.objects.get(id=product_id)

    # convert into dict
    data = {key: value[0] for key, value in request.POST.lists()} #🔄
    if 'csrfmiddlewaretoken' in data: #🔄
        data.pop('csrfmiddlewaretoken') #🔄
    
    variations = [] #🔄
    for category, value in data.items(): #🔄
        variation = Variation.objects.get(product=product, category=category, value=value) #🔄
        variations.append(variation) #🔄
    
    
    
    try:
        cart = Cart.objects.get(session_id=_cart_id(request))      
    except Cart.DoesNotExist:
        cart = Cart.objects.create(session_id=_cart_id(request))
    cart.save()
    
    try:
        
        length = len(variations) #🔄
        cart_item = CartItem.objects.filter(product=product, variations__in = variations).annotate(num=Count('variations')).get(num=length) #🔄
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:
        cart_item = CartItem.objects.create(
            product = product,
            cart = cart,
            quantity = 1
        )
        cart_item.variations.set(variations) #🔄
        cart_item.save()
    return redirect('cart')
def sub_cart(request, item_id):
    cart_item = CartItem.objects.get(pk=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')
def cart_increment(request, item_id):
    cart_item = CartItem.objects.get(pk=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')
def remove_cart_item(request, item_id):
    cart_item = CartItem.objects.get(pk=item_id)
    cart_item.delete()
    return redirect('cart')