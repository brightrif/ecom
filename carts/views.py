from django.shortcuts import render, redirect, get_object_or_404
from store.models import Product
from . models import Cart, CartItem

# Create your views here.

def _cart_id(request):
    # Get the current user's session
    #assigns the value of the session_key attribute of the current user's session to the cart variable. 
    #If there is no active session for the user, the session_key attribute will be None.
    cart = request.session.session_key

    # If no active session for the user,create a new session using the create() method of the request
    if not cart:
        cart = request.session.create()
    return cart

def add_to_cart(request, product_id):

    product = Product.objects.get(id=product_id) #get the product
    
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session

    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request)
        )
    cart.save()
    
 
    cart_item = None
    try:
        cart_item = CartItem.objects.get(product=product, cart=cart)
        cart_item.quantity += 1 
        cart_item.save()
    except CartItem.DoesNotExist:
        pass  # do nothing, let the code continue to the next line
    if cart_item is None:
        cart_item = CartItem.objects.create(
            product=product,
            quantity=1,
            cart=cart,
        )
        cart_item.save()
    
    return redirect('cart')


def remove_from_cart(request, product_id):

    
    cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    product = get_object_or_404(Product, id=product_id) #get the product
    cart_item = CartItem.objects.get(product=product, cart=cart)

    if cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    
    return redirect('cart')

def remove_cart_item(request, product_id):

    
    cart = Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in the session
    product = get_object_or_404(Product, id=product_id) #get the product
    cart_item = CartItem.objects.get(product=product, cart=cart)

    cart_item.delete()
    
    return redirect('cart')

def show_cart(request):
    # Get the current user's session
    cart = request.session.get('cart', {})
    
    # Retrieve the item information from the database
    items = []
    for item_id, quantity in cart.items():
        item = Item.objects.get(id=item_id)
        items.append({
            'item': item,
            'quantity': quantity,
            'subtotal': item.price * quantity,
        })
    
    # Render the shopping cart template
    return render(request, 'cart.html', {'items': items})



def cart(request, total=0, quantity=0, cart_items=None):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        
        tax = (2 * total) / 100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }


    return render (request, 'store/cart.html', context)


