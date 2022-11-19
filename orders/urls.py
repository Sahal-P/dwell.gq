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
        path("admin_order_detailes",views.admin_order_detailes,name="admin_order_detailes"),   
        path("add_address",views.add_address,name="add_address") , 
        path("order_place", views.order_place , name="order_place") ,
        path("order_status", views.order_status, name="order_status"),
        path("order_details/<int:id>", views.order_details , name="order_details"),
        path("admin_orderedit", views.admin_orderedit , name="admin_orderedit"),
        path("ordercancell/<int:id>" , views.ordercancell, name="ordercancell"),
        path("admin_order_cancell", views.admin_order_cancell, name="admin_order_cancell"),
        path("return_order/<int:id>",views.return_order , name="return_order") ,
        path("approve_return" ,views.approve_return, name="approve_return"),
        path("order_success" ,views.order_success, name="order_success"),
        
               
]
