from django.db import models
from django.contrib.auth.models import User # type: ignore
import uuid

#makemigrations -create changes and store in a file 
# migrate - apply the pending changes created by makemigrations

# Create your models here.
class Contact1(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=12)
    suggestion = models.TextField()

    def __str__(self):
        return self.name      #saves record using name 
    
class Registration1(models.Model):
    # id = models.IntegerField(primary_key=(""))
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=122)
    phone = models.CharField(max_length=10)
    password = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Book_service1(models.Model):
    
    id=models.AutoField(primary_key=True)
    User_name = models.CharField(max_length=100)
    # service_plan_id = models.CharField(max_length=100)
    address1 = models.CharField(max_length=200)
    
    
    

    def __str__(self):
        return self.User_name 
    
# class service_plan(models.Model):
#     id=models.AutoField(primary_key=True)
#     service_name=  models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
#     service_details=models.CharField(max_length=200)
    

#     def __str__(self):
#         return self.service_name
        

    
class Items(models.Model):
    id=models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    
    description=models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image= models.ImageField(upload_to='images/')

    def __str__(self):
        return self.name
    
    # models.py


class Service(models.Model):
    service_id=models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name

class ServiceBooking(models.Model):
    SERVICE_CHOICES = [
        ('planting', 'Tree planting'),
        ('tree_pruning', 'tree pruning'),
        ('fertilising', 'Fertilising'),
        ('watering','Watering'),
        ('lawn_care', 'Lawn Maintenance'),
        ('garden_beutification','garden beutification'),
        ('Landscaping','Landscaping')
    ]
    booking_id=models.AutoField(primary_key=True)
    User_name = models.CharField(max_length=100)
    selected_service = models.ForeignKey(Service, on_delete=models.CASCADE)
    address1= models.TextField(max_length=1000)
    price=models.DecimalField(max_digits=10,decimal_places=2)

class P_Type(models.Model):
    id=models.AutoField(primary_key=True)
    t_name = models.CharField(max_length=50)
    
   
    def __str__(self):
        return self.t_name

class Plant(models.Model):
    TYPE_CHOICES=[
        ('aquatic','Aquatic Plants'),
         ('medicinal', 'Medicinal'),
        ('flowering', 'Flowering'),
        ('indoor','Inddor'),
        ('climbers', 'Climbers'),
        ('fruit_bearing','Fruit Bearing'),
        
    ]
    id=models.AutoField(primary_key=True)
    name= models.CharField(max_length=100)
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)
    description=models.CharField(max_length=1000)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    image= models.ImageField(upload_to="image/",null=True, blank=True)

   
class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plant = models.ForeignKey('Plant', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def subtotal(self):
        return self.plant.price * self.quantity
    
    

class Invoice(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    service = models.ForeignKey('Service', on_delete=models.CASCADE)
    address = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice #{self.id} - {self.user.username}"

class PasswordResets(models.Model):
        username = models.ForeignKey(User, on_delete=models.CASCADE)
        reset_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
        created_when = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return f"Password reset for {self.user.username} at {self.created_when}"

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Order #{self.id} by {self.user.username}"
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # snapshot price

    def subtotal(self):
        return self.quantity * self.price