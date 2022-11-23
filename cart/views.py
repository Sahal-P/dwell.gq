from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from category.models import Products
from accounts.models import Address
from django.http import JsonResponse
import razorpay
from django.conf import settings
from . models import Cart, CartItem
# Create your views here.

def _cart_id(request):
    response = HttpResponse()
    user = request.user
    cart = request.COOKIES.get('last_visit')
    if not cart:    
        cart = response.set_cookie('last_visit')
        print(cart)
    return cart

def add_cart(request,id):
    user = request.user
    product = Products.objects.get(id=id)

    if user.is_authenticated:
        try:
            cart_item = CartItem.objects.get(product=product,user=user)
            cart_item.Quantity +=1
            cart_item.save()
        except CartItem.DoesNotExist:
            cart_item = CartItem.objects.create(product=product, Quantity = 1, user= user)
            cart_item.save()
    else:       
            
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id = _cart_id(request))
            cart.save()
            
    return redirect("cart")

def cart(request, total=0,quantity=0,cart_items=None,tax=0,delv=0,g_total=0):
    try :
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id =_cart_id(request))
            
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.selling_price * cart_item.Quantity)
            quantity += cart_item.Quantity
            tax = (5*total)/100
            delv = 5
            g_total = total+ tax+delv
    except  :
        pass
    return render (request,"cart.html", {
        "total":total,
        "quantity":quantity,
        "cart_items":cart_items,
        "delv":delv,
        "tax":tax,
        "g_total":g_total
    })
    
def decrement_cart(request,id):
    
    product = get_object_or_404(Products, id=id)

    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user= request.user)
        else:
            cart = Cart.objects.get(cart_id= _cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart)
            
        if cart_item.Quantity >1:
                cart_item.Quantity -= 1
                cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    
    return redirect ("cart")
    
def delete_cart(request,id):
    
    product=get_object_or_404(Products,id=id)
    if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user)
    else:
        cart=Cart.objects.get(cart_id=_cart_id(request))
        cart_item=CartItem.objects.get(product=product,cart=cart)
    cart_item.delete()
    return redirect('cart')
    
def checkout(request,total=0,quantity=0,cart_items=None,tax=0,delv=0,g_total=0,payment=None):
    
    try :
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        else:
            cart = Cart.objects.get(cart_id =_cart_id())
            
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += (cart_item.product.selling_price * cart_item.Quantity)
            quantity += cart_item.Quantity
            tax = (5*total)/100
            delv = 5
            g_total = total+ tax+delv
        address = Address.objects.filter(user = request.user)
    
        client = razorpay.Client(auth=(settings.RAZOR_ID, settings.RAZOR_SECRET))
        payment = client.order.create({'amount':int(g_total),'currency':'INR' ,'payment_capture' : 1})
        return render(request, "checkout.html", {
        "total":total,
        "quantity":quantity,
        "cart_items":cart_items,
        "delv":delv,
        "tax":tax,
        "g_total":g_total,
        "address" : address,
        "payment": payment,
    })    
    except  :
        return redirect ('cart')
    
def quantity_edit(request):
    id = request.GET.get('id')
    product = get_object_or_404(Products, id=id)
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user= request.user)
    else:
        cart = Cart.objects.get(cart_id= _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
        
    if cart_item.Quantity :
            qty = cart_item.Quantity + 1
            cart_item.Quantity +=1
            cart_item.save()
            total = (cart_item.product.selling_price * cart_item.Quantity)
            tax = (5*total)/100
            delv = 5
            g_total = total+ tax+delv
            cart_item.save()
            sub = cart_item.sub_total()
    
    return JsonResponse({"qty":qty, "total":total , "tax":tax , "delv":delv , "g_total": g_total , "sub":sub})

def quantity_minus(request):
    id = request.GET.get('id')
    product = get_object_or_404(Products, id=id)
    
    if request.user.is_authenticated:
        cart_item = CartItem.objects.get(product=product, user= request.user)
    else:
        cart = Cart.objects.get(cart_id= _cart_id(request))
        cart_item = CartItem.objects.get(product=product, cart=cart)
    
    if cart_item.Quantity :
            qty = cart_item.Quantity - 1
            cart_item.Quantity -=1
            cart_item.save()
            total = (cart_item.product.selling_price * cart_item.Quantity)
            tax = (5*total)/100
            delv = 5
            g_total = total+ tax+delv
            cart_item.save()
            sub = cart_item.sub_total()
 
    return JsonResponse({"qty":qty, "total":total , "tax":tax , "delv":delv , "g_total": g_total , "sub":sub})

def Gusr(request):
    
    if request.user.is_anonymous:
        response = HttpResponse('Visiting for the first time')
        p= Products.objects.get(id=10)
        id = p.id
        response.set_cookie('Guestuser',request.user,id)
        
    return response
        
        
        
