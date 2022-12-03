

from django.urls import path
from . import views




urlpatterns = [ 
       path("product_offer", views.product_offer, name="product_offer"),
       path("category_offer", views.category_offer, name="category_offer"),
       path("add_Product_offer/<int:id>", views.add_Product_offer, name="add_Product_offer"),
       path("add_category_offer/<int:id>", views.add_category_offer, name="add_category_offer"),
       path("remove_category_offer", views.remove_category_offer, name="remove_category_offer"),
       path("remove_product_offer", views.remove_product_offer, name="remove_product_offer"),
]
