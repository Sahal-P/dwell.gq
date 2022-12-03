
from django.urls import path
from . import views


urlpatterns = [ 
       path('',views.coupen, name="coupen"),
       path('add_coupen',views.add_coupen, name="add_coupen"),
       path('Applay_coupen',views.Applay_coupen, name="Applay_coupen"),
       path('remove_coupen',views.remove_coupen, name="remove_coupen"),
]
