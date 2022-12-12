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
import statistics
from xml.dom.minidom import Document
from django.contrib import admin
from django.urls import path,include
from accounts.views import*
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("accounts.urls")),
    path('', include("pages.urls")),
    path('cart/', include("cart.urls")),
    path('category/', include("category.urls")), 
    path('orders/', include("orders.urls")),
    path('wishlist/', include("wishlist.urls")),
    path('user_profile/', include("user_profile.urls")),
    path('user_profile/offer', include("offer.urls")),
    path('user_profile/coupen', include("coupen.urls")),
    path('user_profile/wallet', include("wallet.urls")),
    path('variations/', include("variation.urls")),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)