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


app_name = 'category'

urlpatterns = [ 
        path("add_product",views.add_product,name="add_product"),       
        path("dropdown_P",views.dropdown_P,name="dropdown_P"),  
        path("dropdown_PE",views.dropdown_PE,name="dropdown_PE"),     
        path("add_category",views.add_category,name="add_category"),
        path("add_subcategory",views.add_subcategory,name="add_subcategory"),
        path("edit_category/<int:id>",views.edit_category,name="edit_category"),
       
        path("delete_category/<int:id>",views.delete_category,name="delete_category"),
        path("delete_subcategory/<int:id>",views.delete_subcategory,name="delete_subcategory"),
        path("delete_product",views.delete_product,name="delete_product"),
               
]
