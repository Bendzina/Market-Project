from django.db import models
from django.contrib.auth.models import User
from app.models import Product, Sku, Store
from django.conf import settings


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    store_id = models.ForeignKey(Store, on_delete=models.CASCADE, null=True)

    weight = models.DecimalField(max_digits=10, decimal_places=2, default=1, null=False, help_text="Weight in kg")
    length = models.DecimalField(max_digits=10, decimal_places=2, default=5, null=False, help_text="Length in cm")
    width = models.DecimalField(max_digits=10, decimal_places=2, default=5, null=False, help_text="Width in cm")
    height = models.DecimalField(max_digits=10, decimal_places=2, default=5, null=False, help_text="Height in cm")
    
    created_at = models.DateTimeField(auto_now_add=True)
    

    def __str__(self):
        return f'Cart of user {self.user.username}'
    

class CartItem(models.Model): 
    # userID, productID, 
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, default=1)
    sku = models.ForeignKey('app.Sku', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    # Add shipping information fields to CartItem
    weight = models.DecimalField(max_digits=10, decimal_places=2, default=1, null=False)
    length = models.DecimalField(max_digits=10, decimal_places=2, default=5, null=False)
    width = models.DecimalField(max_digits=10, decimal_places=2, default=5, null=False)
    height = models.DecimalField(max_digits=10, decimal_places=2, default=5, null=False)

    def __str__(self):
        return f"{self.sku.productid.name} - {self.quantity}"

# ////////////////ახალი დამატებები
class Order(models.Model):
    # userID - წაშლა cartID 
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100, choices=[('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} by {self.user.username}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
