
from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [ 
     path("",views.index,name="index"),
     path("shop",views.shop,name="shop"),
     path("signle_P/<int:id>", views.signle_P,name="signle_P"),
     path("mensSC/<int:id>",views.mensSC,name="mensSC"),
     path("MshirtsP/<int:id>",views.MshirtsP,name="MshirtsP"),
     path("c_category",views.c_category,name="c_category"),
     path("productsingle",views.productsingle,name="productsingle"),
     path("about",views.about,name="about"),
     path("blog",views.blog,name="blog"),
     path("contact",views.contact,name="contact"),
     path("a_tables", views.a_tables, name="a_tables"),
     path("category", views.category, name="category"),
     path("subcategory", views.subcategory, name="subcategory"),
     path("product", views.product, name="product"),
     path("add_category", views.add_category, name="add_category"),
     path("add_subcategory", views.add_subcategory, name="add_subcategory"),
     path("add_product", views.add_product, name="add_product"),
     path("edit_subcategory/<int:id>", views.edit_subcategory, name="edit_subcategory"),
     path("edit_product/<int:id>",views.edit_product,name="edit_product"),
     path("user_block",views.user_block, name="user_block"),

               
]
