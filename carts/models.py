from django.db import models
from store.models import Product
# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    # user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # variations = models.ManyToManyField(Variation, blank=True)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

#calculates the subtotal for a CartItem object based on the quantity of the item and the price of the associated Product object. 
#CartItem object has a foreign key relationship with the Product model, and that the Product model has a price attribute.
    def sub_total(self):
        return self.product.price * self.quantity

 