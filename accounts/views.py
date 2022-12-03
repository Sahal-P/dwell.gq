from cProfile import Profile
import email
from django.contrib import messages
from urllib import request
from urllib.request import Request
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse ,JsonResponse
# Create your views here.
from .helpers import *
from .models import Account 
from datetime import datetime, timedelta
from django.http import HttpResponseRedirect
from cart.models import GCart, CartItem
from orders.models import Orders,Products
from category.models import Offer_product
from django.db.models import Count,Sum,Q,F
import ast
from django.http import FileResponse
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from dateutil.relativedelta import relativedelta

def product_offer(request):
    product = Products.objects.all()
    return render(request, 'admin/Product_offer.html',{'products':product})

def add_Product_offer(request,id):
    if request.POST:
        product = Products.objects.get(id = id)
        offer = Offer_product()
        Discount = request.POST.get('Discount')
        offer.discount = Discount
        offer.product = product
        offer.save()
        product.offer = Discount
        product.save()
        return redirect('product_offer')
    product = Products.objects.get(id=id)
    return render(request, "admin/add_Product_offer.html",{"product":product})

def sales_report(request):
    
    orders   = Orders.objects.annotate(sub_total=F('product__selling_price')*F('quantity'),margin_total=F('product__original_price')*F('quantity'),profit=(F('product__selling_price')-F('product__original_price'))*F('quantity')).order_by("-orderd_date")

    if request.GET.get('Month'):
        currentMonth = datetime.now().month
        
        month1 = request.GET.get('Month')
        month = int(month1)
       
        # today   = datetime.now()- relativedelta(months=1)
        orders      = Orders.objects.filter(orderd_date__month=month).annotate(sub_total=F('product__selling_price')*F('quantity'),margin_total=F('product__original_price')*F('quantity'),profit=(F('product__selling_price')-F('product__original_price'))*F('quantity')).order_by("-orderd_date")

    elif request.GET.get('from_date'):
        from_date   = request.GET.get('from_date')
        date_to     = request.GET.get('to_date')
        if not from_date or not date_to:
            messages.info(request,"Please fill from and to date")
            return redirect(request.META.get('HTTP_REFERER')) 
        to_date     = datetime.strptime(date_to , "%Y-%m-%d")
        to_date11   = to_date + timedelta(1)
        orders      = Orders.objects.filter(orderd_date__range=[from_date, to_date11]).annotate(sub_total=F('product__selling_price')*F('quantity'),margin_total=F('product__original_price')*F('quantity'),profit=(F('product__selling_price')-F('product__original_price'))*F('quantity')).order_by("-orderd_date")
    else:
        messages.info(request,"Please input date or month to filter")
        return redirect(request.META.get('HTTP_REFERER')) 
        
        
    page            = Paginator(orders, 6)
    page_list       = request.GET.get('page')
    page            = page.get_page(page_list)
    
    return render(request , "admin/Sales_report.html", {"orders":page})


def d_admin(request):
    if request.user.is_superuser:
        today   = datetime.now() # - relativedelta(months=1)
        
        current = today.strftime("%B %d, %Y")
        date    = Orders.objects.filter(orderd_date__month = today.month).values("orderd_date__date").annotate(orderd_items=Count('id')).order_by("orderd_date__date")
        sales   = Orders.objects.filter(orderd_date__month = today.month).values("orderd_date__date").annotate(sales=Count('id',filter=Q(status ="Deliverd")),cancelled=Count('id' , filter=Q(status ="cancelled")),returns=Count('id' , filter=(Q(status ="Refund In Progress")|Q(status ="Return Aproved")))).order_by("orderd_date__date")
        
        return render(request, "admin/index.html" ,{'date':date,  'sales':sales , 'current':current})
    return redirect("adminlogin")

def home(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
   
        
    return render(request, "index.html")

def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not email or not password :
            messages.error(request, 'Email and Password is required !!')
            return redirect(request.META.get('HTTP_REFERER'))
        check = Account.objects.filter(email=email).exists()
        if check==False:
            messages.error(request, 'email does not exists !')
        if check:
            user = authenticate(request, email=email,password=password)
            if user is not None :
                if user.is_blocked is True:
                    messages.error(request, 'Sorry, You have been Blocked by admin !!')
                    return redirect(request.META.get('HTTP_REFERER'))
                
                if request.COOKIES.get('Guest_checkout'):
                    value = request.COOKIES.get('Guest_checkout')
                    data = ast.literal_eval(value)
                    dest,id = data.values()
                    
                    gcart=GCart.objects.get(Guest_id = id)
                    if CartItem.objects.filter(Guest_id = gcart).exists():
                        a =CartItem.objects.filter(Guest_id = gcart)
                        print(gcart,",<<<<<<<<<<<<<<<<<<<<")
                        for i in a :
                            print(i.product.selling_price)
                            product = i.product
                            qty = i.Quantity
                            if CartItem.objects.filter(product=product, user= user).exists():
                                b=CartItem.objects.get(product=product, user= user)
                                b.Quantity +=qty
                                b.save()
                            else:
                                cart_item=CartItem.objects.create(product=product,Quantity=qty,user=user)
                                cart_item.save()
                        login(request,user)
                        print(type(dest), dest,"<<<<<<<<<<<<<<<<<<")
                        a.delete()
                        response = redirect(dest)
                        response.delete_cookie('Guest_checkout')
                        return response
                    
                else:
                    login(request,user)
                    return redirect("home")
        
            messages.info(request, 'Invalid Password !!')
              
    return render(request,"login.html")

def user_signup(request,*args, **kwargs):
    
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    try:
            if request.POST:
                first_name= request.POST.get("first_name")
                last_name= request.POST.get("last_name")
                email = request.POST.get("email")
                phone_number = request.POST.get("phone_number")
                username = request.POST.get("username")
                password = request.POST.get("password1")
                
                if not first_name or not email or not phone_number or not username or not password:
                    messages.error(request,'Please fill all required fields')
                    return redirect(request.META.get('HTTP_REFERER'))
                
                if Account.objects.filter(phone_number=phone_number).exists():
                    messages.info(request,'a user with this phone number is already exist')
                    return redirect ('user_signup')
                if Account.objects.filter(username=username).exists():
                    messages.info(request,'username is already taken')
                    return redirect ('user_signup')
                if Account.objects.filter(email=email).exists():
                    messages.info(request, 'An account with this email is already exist')
                    return redirect ('user_signup')
                user = Account.objects.create_user(first_name=first_name,last_name=last_name,
                                                   email=email,username= username,
                                                   phone_number=phone_number,
                                                   password=password)
                user.save()
                user = Account.objects.get(email=email,username=username)
                user1 = authenticate(request,email=email,password=password)
                if user1 is not None:
                    otp_handler = otphandler('9544633437').sent_otp_on_phone() # give phone_number instead of real numbers 
                    signupgetuser(email)
                    return redirect("signup_otp_v")
                
            
    except:
        messages.info(request,'Invalid credentials')
    return render(request,"signup.html")

def signup_otp_v(request):
    user = request.user
    print(user)
    if user.is_authenticated:
        return redirect("home")
    email = signupgetuser.email
    

    try:
        otp = otphandler.Otp
        if request.method == "POST":
            otp1 = request.POST.get("otp1")
            otp2 = request.POST.get("otp2")
            otp3 = request.POST.get("otp3")
            otp4 = request.POST.get("otp4")
            if not otp1 or not otp2 or not otp3 or not otp4:
                messages.error(request,'make sure you filled all fields !!')
                return redirect(request.META.get('HTTP_REFERER'))
            otp5 = otp1+otp2+otp3+otp4
            user = Account.objects.get(email=email)
            if otp == otp5:
                login(request,user)
                return render(request,"index.html")
            else:
                messages.error(request,'Invalid otp, make sure it is correct !!')
                return redirect(request.META.get('HTTP_REFERER'))   
    except:
        messages.error(request,'Invalid credentials !!')
        
    return render (request, "signup_otpv.html")

def user_otp(request):
    if request.user.is_authenticated:
      return redirect("home")
    try: 
        if request.POST:
            phone_number = request.POST.get("phone_number")
            phone = Account.objects.filter(phone_number=phone_number).exists()
            
            if phone is True:
                user = Account.objects.get(phone_number=phone_number)
                request.user = user
                otp_handler = otphandler(phone_number).sent_otp_on_phone()
                return redirect("otp_v")
    except:
       pass
    return render(request,'otp.html')

def otp_v(request):
    if request.user.is_authenticated:
         return redirect("home")
     
    phone = otphandler.phone_number
    user = Account.objects.get(phone_number=phone)
    request.user = user
    try:    
        user =request.user
        otp = otphandler.Otp
        if request.method == "POST":
            otp1 = request.POST.get("otp1")
            otp2 = request.POST.get("otp2")
            otp3 = request.POST.get("otp3")
            otp4 = request.POST.get("otp4")
            if not otp1 or not otp2 or not otp3 or not otp4:
                messages.error(request,'make sure you filled all fields !!')
                return redirect(request.META.get('HTTP_REFERER'))
            otp5 = otp1+otp2+otp3+otp4
            if otp == otp5:
                login(request,user)
                return render(request,"index.html")
            else:
                messages.error(request,'Invalid otp, make sure it is correct !!')
                return redirect(request.META.get('HTTP_REFERER'))   
    except:
        messages.error(request,'Invalid credentials !!')
    return render (request, "otpv.html" )

def resendotp(request):
    phone = otphandler.phone_number
    otphandler(phone).sent_otp_on_phone()
    return JsonResponse({phone:phone})

def adminlogin(request):
    if request.POST:
        email= request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(request,email=email,password=password)
        if user is not None:
            if user.is_superuser is True:
               login(request,user)
               return redirect("d_admin")
    return render (request, "admin/login.html")

def adminlogout(request):
    logout(request)
    return redirect(adminlogin)

def log_out(request):
    logout(request)
    return render(request, "login.html")

def log_in(request):
    return redirect('user_login')