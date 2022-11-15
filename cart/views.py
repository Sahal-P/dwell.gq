from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from category.models import Products
from accounts.models import Address
from django.http import JsonResponse


from . models import Cart, CartItem
# Create your views here.

def _cart_id(request):
    response = HttpResponse()
    user = request.user
    cart = request.COOKIES.get('last_visit')
    print(cart,"<<<<<<<<<<<<<<<<<<<<yyyy")
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
            
        
        # return HttpResponse(cart_item.product)
    # exit()
            
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





    
def checkout(request,total=0,quantity=0,cart_items=None,tax=0,delv=0,g_total=0):
    
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
    except  :
        pass
    
    address = Address.objects.filter(user = request.user)
    

    
    
    return render(request, "checkout.html", {
        "total":total,
        "quantity":quantity,
        "cart_items":cart_items,
        "delv":delv,
        "tax":tax,
        "g_total":g_total,
        "address" : address,
    })    
    
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