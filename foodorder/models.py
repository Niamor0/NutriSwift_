from django.db import models
from django.contrib.auth.models import User
from decimal import Decimal

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.user.username
    
class Pizza(models.Model):
    SIZE = (
        ('Regular', 'Regular'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    )
    name = models.CharField(max_length=100)
    price = models.FloatField()
    toppings = models.CharField(max_length=100)
    size = models.CharField(max_length=100, choices=SIZE)
    description = models.TextField()
    image = models.ImageField(upload_to='pizza')

    def __str__(self):
        return self.name
    
class Pasta(models.Model):
    SPICY = (
        ('Yes', 'Yes'),
        ('No', 'No'),
    )
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    spicy = models.CharField(max_length=100, choices=SPICY)
    image = models.ImageField(upload_to='pasta')

    def __str__(self):
        return self.name    

class Burger(models.Model):
    TYPE = (
        ('Veg', 'Veg'),
        ('Non-Veg', 'Non-Veg'),
    )
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    type = models.CharField(max_length=100, choices=TYPE)
    image = models.ImageField(upload_to='burger')

    def __str__(self):
        return self.name        
    
class Dessert(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='dessert')

    def __str__(self):
        return self.name    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="carts")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum(item.subtotal for item in self.items.all())

    def __str__(self):
        return f"Cart {self.id} for {self.user.username}"

class CartItem(models.Model):
    PRODUCT_TYPES = [
        ('Pizza', 'Pizza'),
        ('Pasta', 'Pasta'),
        ('Burger', 'Burger'),
        ('Dessert', 'Dessert'),
    ]

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product_type = models.CharField(max_length=50, choices=PRODUCT_TYPES)
    product_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)  

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"{self.product_type} (ID: {self.product_id}) - Qty: {self.quantity}"

class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Payment_Pending', 'Payment Pending'),
        ('Confirmed', 'Confirmed'),
        ('Preparing', 'Preparing'),
        ('Out_for_Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    PAYMENT_METHODS = [
        ('Cash', 'Cash on Delivery'),
        ('Bkash', 'Bkash Payment'),
        ('Nagad', 'Nagad Payment'),
        ('Card', 'Card Payment'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    cart = models.ForeignKey(Cart, on_delete=models.SET_NULL, null=True, blank=True) 
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS, default='Cash')
    payment_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} for {self.user.username}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_type = models.CharField(max_length=50, choices=CartItem.PRODUCT_TYPES)
    product_id = models.PositiveIntegerField()
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        return self.price * self.quantity

    def __str__(self):
        return f"Order {self.order.id} - {self.product_type} (ID: {self.product_id})"

class Delivery(models.Model):
    DELIVERY_STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Assigned', 'Assigned to Delivery Partner'),
        ('In_Transit', 'In Transit'),
        ('Delivered', 'Delivered'),
        ('Failed', 'Failed'),
        ('Returned', 'Returned'),
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="delivery")
    address = models.TextField()
    delivery_date = models.DateField(blank=True, null=True)
    delivery_time = models.TimeField(blank=True, null=True) 
    delivery_status = models.CharField(
        max_length=50,
        choices=DELIVERY_STATUS_CHOICES,
        default='Pending',
    )
    assigned_delivery_vendor = models.CharField(max_length=100, blank=True, null=True)
    contact_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return f"Delivery for Order {self.order.id} - {self.delivery_status}"


class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='menu_images/')
    price_per_unit = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name



class Catering(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="caterings")
    event_type = models.CharField(max_length=100)
    event_date = models.DateField()
    location = models.TextField()
    menu_items = models.ManyToManyField(MenuItem, related_name='caterings')
    number_of_guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Catering for {self.event_type} on {self.event_date}"
    

class Contact(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Message from {self.first_name} {self.last_name}"
