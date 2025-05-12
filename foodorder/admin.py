from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Pizza)
admin.site.register(Pasta)
admin.site.register(Burger)
admin.site.register(Dessert)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Delivery)
admin.site.register(Catering)
admin.site.register(MenuItem)

admin.site.index_title = "NeutriSwift Admin"
admin.site.site_header = "NeutriSwift Admin Dashboard"
admin.site.site_title = "NeutriSwift Admin Portal"