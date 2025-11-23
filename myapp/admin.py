from django.contrib import admin
from myapp.models import Contact1
from myapp.models import Registration1
from myapp.models import Book_service1
from myapp.models import Plant
from myapp.models import Items
from myapp.models import Service
from myapp.models import ServiceBooking
from myapp.models import P_Type
from myapp.models import PasswordResets
from myapp.models import CartItem
from myapp.models import Invoice
from myapp.models import Order
from myapp.models import OrderItem
from django.utils.html import format_html
# from myapp.models import PasswordResets

# Register your models here.
admin.site.register(Contact1)
admin.site.register(Registration1)
admin.site.register(Book_service1)
admin.site.register(P_Type)
admin.site.register(Plant)
admin.site.register(Items)
admin.site.register(Service)
admin.site.register(ServiceBooking)
admin.site.register(CartItem)
admin.site.register(Invoice)
admin.site.register(PasswordResets)
admin.site.register(Order)
admin.site.register(OrderItem)


class PlantAdmin(admin.ModelAdmin):
    list_display = ('name', 'p_type', 'price', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 60px; height: 60px;" />', obj.image.url)
        return "-"
    
    image_tag.short_description = 'Image'

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'service', 'address', 'price', 'created_at')