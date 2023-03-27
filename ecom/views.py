
from django.shortcuts import render
from store.models import Product # import product module 

def home(request):
    #get all products 
    products = Product.objects.all().filter(is_available=True).order_by('created_date')

    context = {
        'products': products,
    #    'reviews': reviews,
    }
    
    return render(request, 'home.html', context)