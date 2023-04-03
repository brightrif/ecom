from django.shortcuts import render, get_object_or_404
from .models import Product
from category.models import Category

from django.core.paginator import Paginator

from carts.models import CartItem
from carts.views import _cart_id
# Create your views here.

def store(request, category_slug=None):

    categories = None
    products = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
        #following 3 lines used for pagination 
        paginator = Paginator(products, 6) # split the list into pages with 6 products per page
        page = request.GET.get('page') # get the current page number from the request
        paged_products = paginator.get_page(page) # get the products for the current page
        #pagination ends
    else:
        products = Product.objects.all().filter(is_available=True).order_by('created_date')
        #following 3 lines used for pagination 
        paginator = Paginator(products, 6) # split the list into pages with 6 products per page
        page = request.GET.get('page') # get the current page number from the request
        paged_products = paginator.get_page(page) # get the products for the current page
        #pagination ends 
        product_count = products.count()

    context = {
        'products': paged_products,
        'product_count': product_count,
    #    'reviews': reviews,
    }

    return render(request, 'store/store.html', context)

def product_detail(request, category_slug, product_slug):

    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        product_in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
        
    except Exception as e:
        raise e
    

    context = {
        'single_product': single_product,
        'product_in_cart': product_in_cart,
    }

    return render(request, 'store/product_detail.html', context)