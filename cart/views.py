import ast
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from category.models import Products
from accounts.models import Address
from django.http import JsonResponse
import razorpay
from django.conf import settings
from . models import GCart, CartItem
from django.contrib import messages
from bunch import bunchify
from munch import DefaultMunch
from variation.models import Variation
# Create your views here.

def create(request):
    cart=request.session.session_key
    if not cart:
        cart=request.session.create()
    return cart


def add_cart(request):
    user = request.user
    id = request.GET.get('id')
    varient = 0
    v_id_ = 0
    product = Products.objects.get(id=id)
    if request.GET.get('color') and request.GET.get('size'):
        color = request.GET.get('color')
        size = request.GET.get('size')
        if color is not '0' and size is not '0':
            varient  = Variation.objects.get(product=product,color=color,size=size)
            v_id_ = varient.variation_id

    print(varient,v_id_,"9999999999999999999999999")
    if user.is_authenticated:
        try:
            if varient is not 0:
                cart_item = CartItem.objects.get(product=product,user=user,varient_id=v_id_)
                print("firstpart222222222222222222222222")
                if cart_item.varient_id == v_id_:
                    cart_item.Quantity +=1
                    cart_item.save()
                    status = True
                    return JsonResponse({"status":status})
                else:
                    print("secondpart222222222222222222222222")
                    
                    cart_item = CartItem.objects.create(product=product, Quantity = 1, user= user ,varient_id=varient.variation_id ,varient_price=varient.price)
                    cart_item.save()
                    status = False
                    return JsonResponse({"status":status})
            else:
                cart_item = CartItem.objects.get(product=product,user=user,varient_id=0)
                
                print("second222222222222222222222222")
                cart_item.Quantity +=1
                cart_item.save()
                status = True
                return JsonResponse({"status":status})
                

        except CartItem.DoesNotExist:
            if varient is not 0:
                cart_item = CartItem.objects.create(product=product, Quantity = 1, user= user ,varient_id=varient.variation_id ,varient_price=varient.price)
                cart_item.save()
                status = False
                return JsonResponse({"status":status})
            else:
                cart_item = CartItem.objects.create(product=product, Quantity = 1, user= user)
                cart_item.save()
                status = False
                return JsonResponse({"status":status})
                

    else: 
        
        try:
            id=GCart.objects.get(Guest_id = create(request))
            if CartItem.objects.filter(product=product,Guest=id).exists():
                cart_item=CartItem.objects.get(product=product,Guest=id)
                cart_item.Quantity+=1
                cart_item.save()
            else:
                cart_item=CartItem.objects.create(
                product=product,
                Quantity=1,
                Guest=id,)
                cart_item.save()
        except:
            
            id=GCart.objects.create(Guest_id= create(request))
            id.save()
            cart_item=CartItem.objects.create(
                product=product,
                Quantity=1,
                Guest=id,)
            cart_item.save()
        
    return redirect("cart")

def cart(request,Gcart=0, total=0,quantity=0,cart_items=None,tax=0,delv=0,g_total=0):
    try :
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        

        for cart_item in cart_items:
            c_varient = cart_item.varient_id
            if c_varient != "0":
                v = Variation.objects.get(variation_id=cart_item.varient_id)
                v_price = v.price
                cart_item.varient_price=v_price
                cart_item.save()
                
            if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
                total += (cart_item.product.offer_price * cart_item.Quantity)
            else:
                total += (cart_item.product.selling_price * cart_item.Quantity)
            quantity += cart_item.Quantity
            tax = (5*total)/100
            delv = 5
            g_total = total+ tax+delv

    except :
        
        if GCart.objects.filter(Guest_id=create(request)).exists():
            id=GCart.objects.get(Guest_id=create(request))
            cart_items=CartItem.objects.filter(Guest_id=id,is_active=True)
            
            for cart_item in cart_items:
                if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
                    total += (cart_item.product.offer_price * cart_item.Quantity)
                else:
                    total += (cart_item.product.selling_price * cart_item.Quantity)
                quantity += cart_item.Quantity
                tax = (5*total)/100
                delv = 5
                g_total = total+ tax+delv
                
    return render (request,"cart.html", {
        "total":total,
        "quantity":quantity,
        "cart_items":cart_items,
        "delv":delv,
        "tax":tax,
        "g_total":g_total
    })
    
# def decrement_cart(request,id):
    
#     product = get_object_or_404(Products, id=id)

#     try:
#         if request.user.is_authenticated:
#             cart_item = CartItem.objects.get(product=product, user= request.user)
#         else:
#             cart = Cart.objects.get(cart_id= _cart_id(request))
#             cart_item = CartItem.objects.get(product=product, cart=cart)
            
#         if cart_item.Quantity >1:
#                 cart_item.Quantity -= 1
#                 cart_item.save()
#         else:
#             cart_item.delete()
#     except:
#         pass
    
#     return redirect ("cart")
def cartrefresh(request,Gcart=0, total=0,quantity=0,cart_items=None,tax=0,delv=0,g_total=0):
    try :
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
            
        for cart_item in cart_items:
            c_varient = cart_item.varient_id
            if c_varient != "0":
                v = Variation.objects.get(variation_id=cart_item.varient_id)
                v_price = v.price
                cart_item.varient_price=v_price
                cart_item.save()
                
            if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
                total += (cart_item.product.offer_price * cart_item.Quantity)
            else:
                total += (cart_item.product.selling_price * cart_item.Quantity)
            quantity += cart_item.Quantity
            tax = (5*total)/100
            delv = 5
            g_total = total+ tax+delv

    except :
        
        if GCart.objects.filter(Guest_id=create(request)).exists():
            id=GCart.objects.get(Guest_id=create(request))
            cart_items=CartItem.objects.filter(Guest_id=id,is_active=True)
            
            for cart_item in cart_items:
                if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
                    total += (cart_item.product.offer_price * cart_item.Quantity)
                else:
                    total += (cart_item.product.selling_price * cart_item.Quantity)
                quantity += cart_item.Quantity
                tax = (5*total)/100
                delv = 5
                g_total = total+ tax+delv
                
    return render (request,"cartitems.html", {
        "total":total,
        "quantity":quantity,
        "cart_items":cart_items,
        "delv":delv,
        "tax":tax,
        "g_total":g_total
    })
    
def delete_cart(request):
    id = request.GET.get('id')
    v_id = request.GET.get('v_id')
    product=get_object_or_404(Products,id=id)
    if request.user.is_authenticated:
            cart_item=CartItem.objects.get(product=product,user=request.user,varient_id=v_id)
    else:
        id=GCart.objects.get(Guest_id=create(request))
        cart_item=CartItem.objects.get(product=product,Guest_id=id)
    cart_item.delete()
    status = True
    return JsonResponse({"status":status})
    
def checkout(request,total=0,quantity=0,cart_items=None,tax=0,delv=0,g_total=0,payment=None):
    try :   
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
        num = 0
        
        for cart_item in cart_items:
            
            if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
                total += (cart_item.product.offer_price * cart_item.Quantity)
            else:
                total += (cart_item.product.selling_price * cart_item.Quantity)
            quantity += cart_item.Quantity
            tax = (5*total)/100
            delv = 5
            g_total = total+ tax+delv
        address = Address.objects.filter(user = request.user)
        applied = None
        coupen = None
        if 'new_price' in request.session:
            new_price = request.session['new_price']
            coupen = request.session['coupen']

            if new_price is not None:
                g_total = new_price
                applied = True
        try:
            client = razorpay.Client(auth=(settings.RAZOR_ID, settings.RAZOR_SECRET))
            payment = client.order.create({'amount':int(g_total),'currency':'INR' ,'payment_capture' : 1})
        
            return render(request, "checkout.html", {
            "total":total,
            "quantity":quantity,
            "cart_items":cart_items,
            "delv":delv,
            "tax":tax,
            "coupen":coupen,
            "applied":applied,
            "g_total":g_total,
            "address" : address,
            "payment": payment,})
        except:
            messages.error(request,'Poor internet connection please try again')
            return redirect(request.META.get('HTTP_REFERER'))                 
              
            
          
    except :
        
        if not request.user.is_authenticated:
            Guest_id = GCart.objects.get(Guest_id = create(request))
            
            cart_items = CartItem.objects.filter(Guest_id = Guest_id, is_active=True)
            
            for cart_item in cart_items:
                if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
                    total += (cart_item.product.offer_price * cart_item.Quantity)
                else:
                    total += (cart_item.product.selling_price * cart_item.Quantity)
                quantity += cart_item.Quantity
                tax = (5*total)/100
                delv = 5
                g_total = total+ tax+delv
            address = None

            try:
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
                "payment": payment,})
            except:
                messages.error(request,'Poor internet connection please try again')   
                return redirect(request.META.get('HTTP_REFERER'))                 
        
    return redirect ('cart')
    
    
def quantity_edit(request):
    id = request.GET.get('id')
    v_id = request.GET.get('v_id')
    product = get_object_or_404(Products, id=id)
    if request.user.is_authenticated:
        if v_id is not '0':
            varient = Variation.objects.get(variation_id=v_id)
            v_id = varient.variation_id
            cart_item = CartItem.objects.get(product=product, user= request.user,varient_id=v_id)
        else:
            cart_item = CartItem.objects.get(product=product, user= request.user,varient_id=0)
    else:
        Guest_id = GCart.objects.get(Guest_id= create(request))
        cart_item = CartItem.objects.get(product=product, Guest_id=Guest_id)
        
    if cart_item.Quantity :
            qty = cart_item.Quantity + 1
            if cart_item.product.quantity >=qty:
                cart_item.Quantity +=1
                cart_item.save()
                if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
                    total = (cart_item.product.offer_price * cart_item.Quantity)
                else:
                    total = (cart_item.product.selling_price * cart_item.Quantity)
                cart_item.save()
                sub = cart_item.sub_total()
                
                cart_items = CartItem.objects.filter(user=request.user,is_active=True)
                total=0
                for cart_item in cart_items:
                    if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
                        total += (cart_item.product.offer_price * cart_item.Quantity)
                    else:
                        total += (cart_item.product.selling_price * cart_item.Quantity)
                    tax = (5*total)/100
                    delv = 5
                    g_total = total+ tax+delv
                
                return JsonResponse({"qty":qty, "total":total , "tax":tax , "delv":delv , "g_total": g_total , "sub":sub})

def quantity_minus(request):
    id = request.GET.get('id')
    product = get_object_or_404(Products, id=id)
    v_id = request.GET.get('v_id')
    
    if request.user.is_authenticated:
        if v_id is not '0':
            varient = Variation.objects.get(variation_id=v_id)
            v_id = varient.variation_id
            cart_item = CartItem.objects.get(product=product, user= request.user,varient_id=v_id)
        else:
            cart_item = CartItem.objects.get(product=product, user= request.user,varient_id=0)
    else:
        Guest_id = GCart.objects.get(Guest_id= create(request))
        cart_item = CartItem.objects.get(product=product, Guest_id=Guest_id)
    
    if cart_item.Quantity :
        if cart_item.Quantity is not 1:
            qty = cart_item.Quantity - 1
            cart_item.Quantity -=1
            cart_item.save()
            if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
                total = (cart_item.product.offer_price * cart_item.Quantity)
            else:
                total = (cart_item.product.selling_price * cart_item.Quantity)
            cart_item.save()
            sub = cart_item.sub_total()
            
            cart_items = CartItem.objects.filter(user=request.user,is_active=True)
            total=0
            for cart_item in cart_items:
                if cart_item.product.offer_price is not None and cart_item.product.offer_price is not 0:
                    total += (cart_item.product.offer_price * cart_item.Quantity)
                else:
                    total += (cart_item.product.selling_price * cart_item.Quantity)
                tax = (5*total)/100
                delv = 5
                g_total = total+ tax+delv
    
            
 
    return JsonResponse({"qty":qty, "total":total , "tax":tax , "delv":delv , "g_total": g_total , "sub":sub})

def Gusr(request):
    
    if request.user.is_anonymous:
        response = HttpResponse('Visiting for the first time')
        p= Products.objects.get(id=10)
        id = p.id
        response.set_cookie('Guestuser',request.user,id)
        
    return response
        
        
        
