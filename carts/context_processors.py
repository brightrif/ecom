
from .models import Cart, CartItem
from .views import _cart_id


def counter(request):
    cart_count = 0
    #If the user is accessing the admin panel, return an empty dictionary.
    if 'admin' in request.path:
        return {}
    else:
        try:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            #get all the items in the user's cart using the CartItem model,
            #which has a foreign key relationship with the Cart model. 
            #We use filter() to get only the items in the user's current cart.
            cart_items = CartItem.objects.all().filter(cart=cart[:1])
            for cart_item in cart_items:
                cart_count += cart_item.quantity
        except Cart.DoesNotExist:
            cart_count = 0
    return dict(cart_count=cart_count)