from django.contrib import admin

from django.conf.urls.static import static 
from django.conf import settings
from django.urls import path,include
from myapp import views                 #addedmanually

urlpatterns = [
    path("", views.index,name=' home'),
    path("user_index", views.user_index,name=' user_index'),
    path("admin_index", views.admin_index,name=' admin_index'),
    
    path("register", views.register,name=' registration'),
    path("login/", views.loginuser,name='login'),
    path("logout", views.logoutuser,name=' logout'),
    path('forgot_password', views.ForgotPassword, name='forgot_password'),
    path('password-reset-sent/<str:reset_id>/', views.PasswordResetSent, name='password-reset-sent'),
    path('reset-password/<str:reset_id>/', views.PasswordResets, name='reset-password'),
    path("book_service", views.book_service,name=' book_service'),
    # path("service_plan", views.service_plan,name=' service_plan'),
    path("contact", views.contact,name=' contact us'),
    path("about", views.about,name=' about'),
    path("process_booking", views.process_booking, name=' process_booking'),
    path("shop_plant", views.shop_plant,name= 'shop_plant'),
    path("view_plant/<int:plant_id>/", views.view_plant,name= 'view_plant'),
    path("cart", views.view_cart,name= 'view_cart'),
    path("add_plant", views.add_plant,name= 'add_plant'),
    path("add_to_cart", views.add_to_cart,name= 'add_to_cart'),
    path('cart', views.view_cart, name='view_cart'),
    path('clear_cart', views.clear_cart, name='clear_cart'),
    path('update_cart/', views.update_cart, name='update_cart'),
    path('remove_from_cart/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    # path('test_message/', views.test_message, name='test_message'),
    path('invoice_detail/<int:invoice_id>/', views.invoice_detail, name='invoice_detail'),
    path('checkout', views.checkout, name='checkout'),
    


] 
