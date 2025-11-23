from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import logout,authenticate,login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.apps import apps
from django.core.mail import EmailMessage
from django.utils import timezone
from django.urls import reverse
from django.shortcuts import get_object_or_404
import json

from myapp.models import Contact1
from myapp.models import CartItem
from myapp.models import Plant
from myapp.models import Registration1
from myapp.models import Book_service1
from myapp.models import ServiceBooking,Service,Invoice
from myapp.models import Plant, P_Type
from django.db.models import Q

# from myapp.models import service_plan
# from myapp.models import PasswordResets
from .forms import CreateUserForm



# Create your views here.
def index(request):

    #context is used to set values to a variable 
    #we can fetch values from database and pass it to a variable and print it in the front end 
    # context={'variable':'this is sent'
    #context is passes in return render after file name 
    #          }

   
    return render(request,'index.html')
    # return HttpResponse("this is home page")


def user_index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    messages.success(request, "Login successful! ")    
    return render(request,'user_index.html')


def admin_index(request):
    return render(request,'admin_index.html')


def register(request):
    # form= CreateUserForm
    # return HttpResponse("this is login page")
    if request.method == "POST" :
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        Username = request.POST.get('Username')
        email= request.POST.get('email')
        # phone= request.POST.get('phone')
        password= request.POST.get('password')

        if not Username or not password:
            messages.error(request, "All fields are required.")
            return render(request, "register.html")
        
        user_data_has_error = False
        if User.objects.filter(username=Username).exists():
            user_data_has_error = True
            messages.error(request, 'Username already exists')

        if User.objects.filter(email=email).exists():
            user_data_has_error = True
            messages.error(request, 'Email already exists')

        if password and len(password) < 5:
            user_data_has_error = True
            messages.error(request, 'Password must be at least 5 characters')

        if user_data_has_error:
            return redirect("/register")
        else:
            new_user=User.objects.create_user(first_name = first_name,
                                              last_name=last_name,
                                              username =Username, 
                                              email =email ,
                                            #   phone =phone, 
                                              password =password)
        messages.success(request,"Account created successfully.Login Now")
        return redirect("/login/")
        # user= Registration1(name= name,Username= Username, email=email ,phone=phone, password=password)
        # user.save()
    #     form = CreateUserForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    # context= {'form' : form}
    return render(request,'register.html')


def loginuser(request):
    # return HttpResponse("this is login page")
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        #check if login credientials are equal to admin
        if username == "pallavi" and password == "pallavi":
            # Optionally, set session or flag if needed
            request.session['is_admin'] = True
            messages.success(request, f"Admin login successfull !")
            return render(request, 'admin_index.html')



        # check is user has entered correct credentials
        user = authenticate(username=username , password= password)

        if user is not None:
            # A backend authenticated the credentials
            login(request,user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("/user_index")
        else:

            messages.error(request,"Invalid Login Credentials")
            # No backend authenticated the credentials
            return redirect("/login/")

    # return redirect("/login")
    return render(request, "login.html")


def logoutuser(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("/")
    # return HttpResponse("this is logout page")


def ForgotPassword(request):
    
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user = User.objects.get(email=email)

            new_password_reset = PasswordResets(username = user)
            new_password_reset.save()

            password_reset_url = reverse('reset-password', kwargs={'reset_id': new_password_reset.reset_id})

            full_password_reset_url = f'{request.scheme}://{request.get_host()}{password_reset_url}',

            email_body = f'Reset your password using the link below:\n\n\n{full_password_reset_url}',
        
            email_message = EmailMessage(
                'Reset your password', # email subject
                email_body,
                settings.EMAIL_HOST_USER, # email sender
                [email] # email  receiver 
            )

            email_message.fail_silently = True
            email_message.send()

            return redirect('password-reset-sent', reset_id=new_password_reset.reset_id)

        except User.DoesNotExist:
            messages.error(request, f"No user with email '{email}' found")
            return redirect('forgot_password')

    return render(request, 'forgot_password.html')


def PasswordResetSent(request, reset_id):
    if PasswordResets.objects.filter(reset_id=reset_id).exists():
        return render(request, 'password_reset_sent.html')
    else:
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')


def PasswordResets(request, reset_id):
    try:
        password_reset_id = PasswordResets.objects.get(reset_id=reset_id)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            passwords_have_error = False

            if password != confirm_password:
                passwords_have_error = True
                messages.error(request, 'Passwords do not match')

            if len(password) < 5:
                passwords_have_error = True
                messages.error(request, 'Password must be at least 5 characters long')

            expiration_time = password_reset_id.created_when + timezone.timedelta(minutes=10)

            if timezone.now() > expiration_time:
                passwords_have_error = True
                messages.error(request, 'Reset link has expired')

                password_reset_id.delete()

            if not passwords_have_error:
                user = password_reset_id.user
                user.set_password(password)
                user.save()

                password_reset_id.delete()

                messages.success(request, 'Password reset. Proceed to login')
                return redirect('login')
            else:
                # redirect back to password reset page and display errors
                return redirect('reset-password', reset_id=reset_id)

    
    except PasswordResets.DoesNotExist:
        
        # redirect to forgot password page if code does not exist
        messages.error(request, 'Invalid reset id')
        return redirect('forgot-password')

    return render(request, 'reset_password.html')



def book_service(request):
    if request.user.is_anonymous:
        return redirect("/login/")
    
    if request.method == "POST":
        print("✅ POST request received")

        service_id = request.POST.get('service')
        address = request.POST.get('address1')
        print("📦 Received service ID from form:", service_id)
        
        try:
            service = Service.objects.get(service_id=int(service_id))
        except (Service.DoesNotExist, ValueError, TypeError) as e:
            print(f"❌ Error fetching service: {e}")
            messages.error(request, "Invalid service.")
            return redirect('book_service')

        # create booking
       

        invoice = Invoice.objects.create(
            user=request.user,
            service=service,
            address=address,
            price=service.price
        )

      

        messages.success(request, "Invoice generated. Please proceed to payment.")
        return redirect('invoice_detail', invoice_id=invoice.id)
    
    # GET request
    services = Service.objects.all()
    services_json = json.dumps([
        {'service_id': s.service_id, 'name': s.name, 'description': s.description, 'price': str(s.price),
         }
        for s in services
    ])
    return render(request, 'book_service.html', {
        'services': services,
        'services_json': services_json,
        'user': request.user
    })

            # service_details =request.POST.get('service_details')
            # book_serv= ServiceBooking(User_name= User_name, address1=address1,selected_service=selected_service,price=price)
            # book_serv.save()
        # return render(request,'book_service.html')
    
    # return render(request,'book_service.html')


def about(request):
    return HttpResponse("this is about page")

def shop_plant(request):
    query = request.GET.get('q', '')  # get search text

    if query:
        plants = Plant.objects.filter(
            Q(name__icontains=query) |
            Q(type__icontains=query)
        )
    else:
        plants = Plant.objects.all()
    
    cart_count = 0
    if request.user.is_authenticated:
        from .models import CartItem
        cart_count = CartItem.objects.filter(user=request.user).count()
    
    return render(request, 'product.html', {
        'plants': plants,
        'cart_count': cart_count
    })
# return render(request,'product.html',{'plants': objplant})


def add_to_cart(request):

    if request.user.is_anonymous:
        messages.success(request, "You need to login first to add items to cart")
        return redirect("/login/")
    if request.method == 'POST':
        plant_id = request.POST.get('plant_id')
        plant = get_object_or_404(Plant, id=plant_id)

        cart_item, created = CartItem.objects.get_or_create(
            user=request.user,
            plant=plant,
            defaults={'quantity': 1}
        )

        if not created:
            cart_item.quantity += 1
            cart_item.save()

        messages.success(request, f"{plant.name} added to cart.")
        return redirect('/shop_plant')  
    
def view_plant(request,plant_id):
    plant = get_object_or_404(Plant, id=plant_id)
   
    return render(request,'shop.html',{'plant': plant})

def view_cart(request):
    if request.user.is_anonymous:
        messages.success(request, "Login to see the Cart First ")
        return redirect("/login/")
    else:
        cart_items = CartItem.objects.filter(user=request.user)
        total = sum(item.subtotal() for item in cart_items)
        return render(request, 'cart.html', {'cart_items': cart_items, 'total': total})


def clear_cart(request):
    if request.user.is_anonymous:
        messages.success(request, "Login to see the Cart First ")
        return redirect("/login/")
    CartItem.objects.filter(user=request.user).delete()
    messages.success(request, "Your cart has been cleared.")
    return redirect('view_cart')

def update_cart(request):
    for key, value in request.POST.items():
        if key.startswith('quantity_'):
            try:
                item_id = int(key.split('_')[1])
                quantity = int(value)

                cart_item = CartItem.objects.get(id=item_id, user=request.user)

                if quantity > 0:
                    cart_item.quantity = quantity
                    cart_item.save()
                else:
                    cart_item.delete()  # remove if quantity is zero
            except (ValueError, CartItem.DoesNotExist):
                continue  # ignore invalid form keys

    messages.success(request, "Cart updated successfully.")
    return redirect('view_cart')


def remove_from_cart(request, item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id, user=request.user)
        cart_item.delete()
        messages.success(request, "Item removed from cart.")
    except CartItem.DoesNotExist:
        messages.error(request, "Item not found in your cart.")
    return redirect('view_cart')


def checkout(request):
    cart_items = CartItem.objects.filter(user=request.user)
    total = sum(item.subtotal() for item in cart_items)

    # Handle buy now for single plant
    if request.method == 'POST' and 'plant_id' in request.POST:
        plant_id = request.POST.get('plant_id')
        plant = get_object_or_404(Plant, id=plant_id)
        cart_items = [{'plant': plant, 'quantity': 1, 'subtotal': plant.price}]
        total = plant.price

    if request.method == 'POST' and 'plant_id' not in request.POST:
        # Place order from cart
        from myapp.models import Order
        from myapp.models import OrderItem
        order = Order.objects.create(user=request.user, total=total)
        for item in CartItem.objects.filter(user=request.user):
            OrderItem.objects.create(order=order, plant=item.plant, quantity=item.quantity, price=item.plant.price)
        CartItem.objects.filter(user=request.user).delete()
        messages.success(request, "Order placed successfully!")
        return redirect('/shop_plant')

    return render(request, 'checkout.html', {'cart_items': cart_items, 'total': total})

def contact(request):
    # return HttpResponse("this is contact us  page")
    if request.user.is_anonymous:
        messages.success(request, "you will need to login first ")
        return redirect("/login/")
    else:
        if request.method == "POST" :
            name = request.POST.get('name')
            email= request.POST.get('email')
            phone= request.POST.get('phone')
            suggestion= request.POST.get('suggestion')
            contact= Contact1(name= name, email=email ,phone=phone, suggestion=suggestion)
            contact.save()
            messages.success(request, "your message has been sent ")

    return render(request,'contact.html')


def add_plant(request):
    plant_types=P_Type.objects.all()

    if request.method == "POST" :
        image=request.FILES.get('image')
        type_id = request.POST.get('p_type')
        print("📥 Received type_id:", type_id)

        # name = request.POST.get('name')
        # # type_id= request.POST.get('p_type')
        # description= request.POST.get('description')
        # price= request.POST.get('price')
        # image= request.POST.get('image')


        try:
           selected_type = P_Type.objects.get(id=type_id)
            
        except (P_Type.DoesNotExist, ValueError, TypeError) as e:
            messages.error(request, "Selected plant type does not exist.")
            
            return HttpResponse("type not found or invalid ID", status=404)

        plant = Plant(
            name = request.POST.get('name'),
            type= selected_type,
            description= request.POST.get('description'),
            price= request.POST.get('price'),
            image= image
        )
        plant.save()
        messages.success(request, "Plant has been successfully added to the database!")

       

        types=P_Type.objects.all()
        return render(request, 'addplant.html', {'P_Type': plant_types,})
    
    

    types=P_Type.objects.all()
    types_json=json.dumps([
        {'id': t.id, 't_name': t.t_name, 
         }
        for t in types
    ])
    return render(request, 'addplant.html', {
        'P_Type': types,
        'plants_json': types_json,
        
    })

def process_booking(request):
    # return HttpResponse("this is logout page")
    return render(request,'process_booking.html')



def invoice_detail(request, invoice_id):
    invoice = get_object_or_404(Invoice,id=invoice_id, user=request.user)
    if request.method == 'POST':
        # ✅ Save booking now
        ServiceBooking.objects.create(
            User_name=request.user.username,
            selected_service=invoice.service,
            address1=invoice.address,
            price=invoice.price
        )
        messages.success(request, "Payment successful! Booking confirmed.click home ")
        return render(request, 'invoice.html', {'invoice': invoice}) # or a thank-you page

    return render(request, 'invoice.html', {'invoice': invoice})

def admin_index(request):
    models_info = []

    # Get all models from the current app
    for model in apps.get_models():
        model_name = model.__name__
        fields = [field.name for field in model._meta.fields]
        data = model.objects.all()
        models_info.append({
            'name': model_name,
            'fields': fields,
            'data': data
        })

    return render(request, 'admin_index.html', {'models_info': models_info})