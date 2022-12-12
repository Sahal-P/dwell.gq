from django.urls import path
from . import views




urlpatterns = [ 
        path("",views.variation,name="variation"),  
        path("types",views.types,name="types"),  
        path("addTypes",views.addTypes,name="addTypes"), 
        path("check_variation", views.check_variation, name="check_variation"), 

    ]
