
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
        path("guest_checkout", views.guest_checkout, name= "guest_checkout"),
        path('order_invoice/<str:id>', views.order_invoice, name="order_invoice")
        
               
]
