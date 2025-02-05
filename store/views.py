from django.shortcuts import get_object_or_404, render
from category.models import Category
from .models import Product
from cart.models import CartItem
from cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


def product_detail(request, category_slug, product_slug):
    product = get_object_or_404(Product, slug=product_slug, category__slug=category_slug)    
    in_cart = CartItem.objects.filter(cart__session_id = _cart_id(request), product = product).exists()
    context = {
        'product': product,
        'in_cart': in_cart
    }
    return render(request, 'product_detail.html', context)

def store(request, category_slug=None):
    if category_slug == None:
        products = Product.objects.filter(is_available=True)
    else:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(is_available=True, category=categories)
    paginator =  Paginator(products, 9)
    page_num = request.GET.get('page')
    paged_products = paginator.get_page(page_num)
    context = {
        'products': paged_products,
        'product_count': products.count()
    }
    return render(request, 'store.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET.get('keyword')
    if keyword:
        products = Product.objects.filter(Q(name__icontains=keyword) | Q(description__icontains=keyword))
    
    context = {
        'products': products,
        'product_count': products.count()
    }
    return render(request, 'store.html', context)