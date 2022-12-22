
from django.urls import path
from . import views


app_name = 'category'

urlpatterns = [ 
        path("add_product",views.add_product,name="add_product"),       
        path("dropdown_P",views.dropdown_P,name="dropdown_P"),  
        path("dropdown_PE",views.dropdown_PE,name="dropdown_PE"),     
        path("add_category",views.add_category,name="add_category"),
        path("add_subcategory",views.add_subcategory,name="add_subcategory"),
        path("edit_category/<int:id>",views.edit_category,name="edit_category"),
       
        path("delete_category",views.delete_category,name="delete_category"),
        path("delete_subcategory",views.delete_subcategory,name="delete_subcategory"),
        path("delete_product",views.delete_product,name="delete_product"),
               
]
