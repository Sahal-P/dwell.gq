

from django.urls import path
from . import views


urlpatterns = [ 
     path("", views.cart, name="cart"),
     path("add_cart",views.add_cart,name="add_cart"),
     path("checkout" ,views.checkout , name="checkout"),
     path("quantity_edit" ,views.quantity_edit , name="quantity_edit"),
    #  path("decrement_cart/<int:id>", views.decrement_cart , name ="decrement_cart"),
     path("delete_cart", views.delete_cart, name="delete_cart"),
     path("quantity_minus", views.quantity_minus, name="quantity_minus"),
     path("Gusr", views.Gusr, name="Gusr"),
     path("cartrefresh",views.cartrefresh,name="cartrefresh")
     
               
]
