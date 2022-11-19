from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import JsonResponse
from accounts.models import Wishlist
from category.models import Products


def add_to_wishlist(request):
    id = request.GET.get('id')
    wished_item = Products.objects.get(id=id)
    checkwish = Wishlist.objects.filter(wished_item=wished_item , user = request.user).exists()
    if checkwish is True:
        return 
    else:
        wishlist = Wishlist.objects.create(wished_item=wished_item, user=request.user ,quantity = 1)
        return JsonResponse({"id":id})

def wishlist(request):
    try:
        wish = Wishlist.objects.filter(user=request.user).order_by('-added_date')
        return render(request, "wishlist.html", {'wish':wish})
    except:
        wish = None
        return render(request, "wishlist.html", {'wish': wish})

def delete_wish(request):
    id = request.GET.get("id")
    wish = Wishlist.objects.get(id=id)
    wish.delete()
    return JsonResponse({None})