"""dwell URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views


urlpatterns = [ 
     path("", views.cart, name="cart"),
     path("add_cart/<int:id>",views.add_cart,name="add_cart"),
     path("checkout" ,views.checkout , name="checkout"),
     path("quantity_edit" ,views.quantity_edit , name="quantity_edit"),
     path("decrement_cart/<int:id>", views.decrement_cart , name ="decrement_cart"),
     path("delete_cart/<int:id>", views.delete_cart, name="delete_cart"),
     path("quantity_minus", views.quantity_minus, name="quantity_minus"),
     
               
]
