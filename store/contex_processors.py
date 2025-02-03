from django.core.exceptions import ObjectDoesNotExist
from cart.views import _cart_id
from cart.models import CartItem, Cart


def counter(request):
    cart_count = 0
    try:
            
        cart = Cart.objects.get(session_id=_cart_id(request))            
        cart_items = CartItem.objects.filter(cart=cart)
            
        for cart_item in cart_items:
            cart_count += cart_item.quantity
            
    except ObjectDoesNotExist:
            cart_count = 0
            
    return dict(cart_count = cart_count)