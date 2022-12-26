import email
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse ,JsonResponse
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from .helpers import *
from .models import Account ,ReferalSection,Banner
from datetime import datetime, timedelta
from cart.models import GCart, CartItem
from orders.models import Orders,Products
from category.models import Offer_product,SubCategory,Category
from django.db.models import Count,Sum,Q,F
import ast
from django.core.paginator import Paginator
from wallet.models import Wallet
import uuid
from django.core.mail import send_mail

def page_not_found_view(request, exception):
    return render(request, 'page-not-found.html', status=404)

def error_500(request):
    return render(request, 'page-not-found.html')

@never_cache
@login_required(login_url='adminlogin')
def product_offer(request):
    product = Products.objects.all()
    return render(request, 'admin/Product_offer.html',{'products':product})

@never_cache
@login_required(login_url='adminlogin')
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

@never_cache
@login_required(login_url='adminlogin')
def sales_report(request):
    
    orders   = Orders.objects.annotate(sub_total=F('product__selling_price')*F('quantity'),margin_total=F('product__original_price')*F('quantity'),profit=(F('product__selling_price')-F('product__original_price'))*F('quantity')).order_by("-orderd_date")
    
    if  request.GET.get('Month') != "0":
        currentMonth = datetime.now().month
        month1 = request.GET.get('Month') 
        if month1 is not None and month1 !="0":
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
   
        
        
    page            = Paginator(orders, 6)
    page_list       = request.GET.get('page')
    page            = page.get_page(page_list)
    
    return render(request , "admin/Sales_report.html", {"orders":page})

@never_cache
@login_required(login_url='adminlogin')
def d_admin(request):
    if request.user.is_superuser:
        today   = datetime.now() # - relativedelta(months=1)
        current = today.strftime("%B %d, %Y")
        date    = Orders.objects.filter(orderd_date__month = today.month).values("orderd_date__date").annotate(orderd_items=Count('id')).order_by("orderd_date__date")
        sales   = Orders.objects.filter(orderd_date__month = today.month).values("orderd_date__date").annotate(sales=Count('id',filter=Q(status ="Deliverd")),cancelled=Count('id' , filter=Q(status ="cancelled")),returns=Count('id' , filter=(Q(status ="Refund In Progress")|Q(status ="Return Aproved")))).order_by("orderd_date__date")
        best_moving = Orders.objects.filter(orderd_date__year = today.year).annotate(moving = Count('product_id' )).filter(moving__gt = 2)
        return render(request, "admin/index.html" ,{'date':date,  'sales':sales , 'current':current,"best_moving":best_moving})
    return redirect("adminlogin")

@never_cache
def home(request):
    id = 16
    id2 = 19
    trending = Products.objects.all().order_by('?')[:6]
    our = Products.objects.filter(subcategory_id =16).order_by('?')[:3]
    banner = Banner.objects.all()[:3]
    banner2 = Banner.objects.all()[3:6]
    catag = Category.objects.all()
    subcat = SubCategory.objects.all()
    new_prod = Products.objects.all().order_by('-added_Date')[:9]
   
    if request.user.is_authenticated:
        
        return render(request, "index.html",{"id":id,"id2":id2,"trending":trending,"our":our ,"banner1":banner,"banner2":banner2,"catag":catag,"subcat":subcat,"new_prod":new_prod})
    return render(request, "index.html",{"id":id,"id2":id2,"trending":trending,"our":our , "banner1":banner,"banner2":banner2,"catag":catag,"subcat":subcat,"new_prod":new_prod})

@never_cache
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
                        trans_carts =CartItem.objects.filter(Guest_id = gcart)
                        for i in trans_carts :
                            product = i.product
                            qty = i.Quantity
                            if CartItem.objects.filter(product=product, user= user ,varient_id=i.varient_id).exists():
                                new_cart=CartItem.objects.get(product=product, user= user,varient_id=i.varient_id)
                                new_cart.Quantity +=qty
                                new_cart.save()
                            else:
                                cart_item=CartItem.objects.create(product=product,Quantity=qty,user=user,varient_id=i.varient_id)
                                cart_item.save()
                        login(request,user)
                        trans_carts.delete()
                        response = redirect(dest)
                        response.delete_cookie('Guest_checkout')
                        return response
                    
                else:
                    login(request,user)
                    return redirect("home")
        
            messages.info(request, 'Invalid Password !!')
              
    return render(request,"login.html")

@never_cache
def user_signup(request,*args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    try:
            if request.POST:
                amount = 0
                if request.POST.get('Referal'):
                    referal_id = request.POST.get('Referal')
                    
                    if ReferalSection.objects.filter(referal_id=referal_id).exists():
                        amount = 500
                    else:
                        messages.error(request,'Enterd Referal id is Invalid')
                        return redirect(request.META.get('HTTP_REFERER'))
                        
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
                
                if amount is not 0:
                    wallet = Wallet.objects.create(user=user,amount = amount)
                    wallet.save()
                    
                user = Account.objects.get(email=email,username=username)
                
                user1 = authenticate(request,email=email,password=password)
                if user1 is not None:
                    otp_handler = otphandler(phone_number).sent_otp_on_phone()
                    response = redirect("signup_otp_v")
                    response.set_cookie('phone', phone_number)
                    signupgetuser(email,phone_number)
                    return response
                
    except:
        messages.info(request,'Invalid credentials')
    return render(request,"signup.html")

@never_cache
def signup_otp_v(request):
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    email = signupgetuser.email
    phone_number = request.COOKIES.get('phone')
    try:
        user = Account.objects.get(phone_number=phone_number)
    except:
        messages.error(request,'somthing error occured during the verification !!')
        return redirect(request.META.get('HTTP_REFERER'))
    request.user = user
    

    try:
        if request.method == "POST":
            otp1 = request.POST.get("otp1")
            otp2 = request.POST.get("otp2")
            otp3 = request.POST.get("otp3")
            otp4 = request.POST.get("otp4")
            otp5 = request.POST.get("otp5")
            otp6 = request.POST.get("otp6")
            if not otp1 or not otp2 or not otp3 or not otp4 or not otp5 or not otp6:
                messages.error(request,'make sure you filled all fields !!')
                return redirect(request.META.get('HTTP_REFERER'))
            
            code = otp1+otp2+otp3+otp4+otp5+otp6
            check = otphandler(phone_number).checkotp(code)
            if check == True:
                login(request,user)
                credit = 100
                if Wallet.objects.filter(user=user).exists():
                    
                    wallet = Wallet.objects.get(user=user)
                    wallet.amount += credit
                    wallet.save()
                else:                    
                    wallet = Wallet.objects.create(user=user,amount = credit)
                wallet.save()
                refer_id = str(user.first_name) + str(uuid.uuid4())[:8]
                
                referal = ReferalSection.objects.create(user=user,referal_id = refer_id)
                referal.save()
                if request.COOKIES.get('Guest_checkout'):
                    value = request.COOKIES.get('Guest_checkout')
                    data = ast.literal_eval(value)
                    dest,id = data.values()
                    
                    gcart=GCart.objects.get(Guest_id = id)
                    if CartItem.objects.filter(Guest_id = gcart).exists():
                        trans_carts =CartItem.objects.filter(Guest_id = gcart)
                        for i in trans_carts :
                            product = i.product
                            qty = i.Quantity      
                            cart_item=CartItem.objects.create(product=product,Quantity=qty,user=user,varient_id=i.varient_id)
                            cart_item.save()
                        trans_carts.delete()
                        response = redirect(dest)
                        response.delete_cookie('phone')
                        response.delete_cookie('Guest_checkout')
                        return response
                    
                response = render(request,"index.html")
                response.delete_cookie('phone')

                return response
            else:
                messages.error(request,'Invalid otp, make sure it is correct !!')
                return redirect(request.META.get('HTTP_REFERER'))   
    except:
        messages.error(request,'Invalid credentials !!')
        
    return render (request, "signup_otpv.html")

@never_cache
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
                
                response = redirect("otp_v")
                response.set_cookie('phone', phone_number)
                signupgetuser(email,phone_number)
                return response
            else :
                messages.error(request,'User does not exists in this number !!')
                return redirect(request.META.get('HTTP_REFERER'))
                
    except:
       pass
    return render(request,'otp.html')

@never_cache
def otp_v(request):
    if request.user.is_authenticated:
         return redirect("home")
     
    phone_number = request.COOKIES.get('phone')
    try:
        user = Account.objects.get(phone_number=phone_number)
    except:
        messages.error(request,'somthing error occured during the verification !!')
        return redirect(request.META.get('HTTP_REFERER'))
    request.user = user

    try:    
        user =request.user
        if request.method == "POST":
            otp1 = request.POST.get("otp1")
            otp2 = request.POST.get("otp2")
            otp3 = request.POST.get("otp3")
            otp4 = request.POST.get("otp4")
            otp5 = request.POST.get("otp5")
            otp6 = request.POST.get("otp6")
            if not otp1 or not otp2 or not otp3 or not otp4 or not otp5 or not otp6:
                messages.error(request,'make sure you filled all fields !!')
                return redirect(request.META.get('HTTP_REFERER'))
            
            code = otp1+otp2+otp3+otp4+otp5+otp6
            check = otphandler(phone_number).checkotp(code)
            if check is True:
                login(request,user)
                response = render(request,"index.html")
                response.delete_cookie('phone')
                return response
            else:
                messages.error(request,'Invalid otp, make sure it is correct !!')
                return redirect(request.META.get('HTTP_REFERER'))   
    except:
        messages.error(request,'Invalid credentials !!')
    return render (request, "otpv.html" )


def resendotp(request):
    phone = otphandler.phone_number
    phone_number = request.COOKIES.get('phone')
    
    otphandler(phone).sent_otp_on_phone()
    return JsonResponse({phone:phone})

@never_cache
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

@never_cache
def adminlogout(request):
    logout(request)
    return redirect("adminlogin")

@never_cache
def log_out(request):
    logout(request)
    return render(request, "login.html")

@never_cache
def log_in(request):
    return redirect('user_login')

@never_cache
@login_required(login_url='adminlogin')
def banner(request):
    banner = Banner.objects.all()
    return render(request, "admin/banner.html",{"banner":banner})

@never_cache
@login_required(login_url='adminlogin')
def add_banner(request):
    count = len(Banner.objects.all())
    if count >= 6:
        messages.error(request,"6 Banners Added Please Remove one to add New")
        return redirect(request.META.get('HTTP_REFERER')) 
    if request.POST.get('banner_name'):    
        name = request.POST.get('banner_name')
    else:
        messages.error(request,"Banner name is required ")
        return redirect('banner') 
    if request.FILES.get('ban_img1'):    
        img = request.FILES.get('ban_img1')
    else:
        messages.error(request,"Banner Image is required ")
        return redirect('banner') 
    
    if request.POST.get('banner_validity'):    
        validity = request.POST.get('banner_validity')
    else:
        messages.error(request,"Banner Validity date is required ")
        return redirect('banner') 
    
    if request.POST.get('Select1'):    
        select1 = request.POST.get('Select1')
    else:
        messages.error(request,"Select Banner wise required")
        return redirect('banner') 
    
    if request.POST.get('Select1'):    
        select2 = request.POST.get('Select2')
    else:
        messages.error(request,"Select Banner wise Product or Category")
        return redirect('banner') 
    banner_id = str(uuid.uuid4())
    banner = Banner.objects.create(banner_name=name,image = img , validity_upto = validity,wise = select1,selected = select2,banner_id = banner_id)
    banner.save()
    messages.info(request,"Banner added ")
    return redirect('banner') 

@login_required(login_url='adminlogin')
def BannerSelect(request):
    selected = request.GET.get('selected')
    if selected == "Product":
        item = Products.objects.all()
        wise = "Product"
    if selected == "Category":
        item = SubCategory.objects.all()
        wise = "Cata"
        
    return render (request,"admin/bannerselect.html",{"item":item,"wise":wise})

@login_required(login_url='adminlogin')
def Remove_banner(request):
    id = request.GET.get('id')
    banner = Banner.objects.get(id = id)
    banner.delete()
    status = True
    messages.info(request,"Banner Removed ")
    return redirect(request.META.get('HTTP_REFERER'))   


def searchproduct(request):
    data = request.GET.get('searched')
    if data =='':
        messages.warning(request,"please type somthing in the search box")
        return redirect(request.META.get('HTTP_REFERER'))
    id =0
    if request.GET.get('id_subc'):
        id = request.GET.get('id_subc')
        if id is not None and id != "0":
            subcat = SubCategory.objects.get(id = id )
            product = Products.objects.filter(product_name__icontains = data,subcategory=subcat).annotate(mrp=F('selling_price')+300).order_by('id')
        else:    
            product = Products.objects.filter(product_name__icontains = data).annotate(mrp=F('selling_price')+300).order_by('id')
            
    elif request.GET.get('id_catg'):
        id = request.GET.get('id_catg')
        if id is not None and id != "0":
            catg = Category.objects.get(id = id )
            product = Products.objects.filter(product_name__icontains = data,category=catg).annotate(mrp=F('selling_price')+300).order_by('id')
        else:    
            product = Products.objects.filter(product_name__icontains = data).annotate(mrp=F('selling_price')+300).order_by('id')
        
    else:    
            product = Products.objects.filter(product_name__icontains = data).annotate(mrp=F('selling_price')+300).order_by('id')
    
    if not product:
        messages.warning(request,"No result Found !!")
        return redirect(request.META.get('HTTP_REFERER'))
    for i in product:
        if i.category.discount<i.offer:
         if i.offer is not None and i.offer is not 0 :
            i.offer_price = int(i.original_price - i.original_price * i.offer/100)
            i.save()
            continue
        if i.category.discount is not None:
            i.category_offer = i.category.discount
            if i.category.discount is not 0:
                i.offer_price = int(i.original_price - i.original_price * i.category.discount/100)
            else:
                 i.offer_price = i.category.discount
            i.save()
    # product= Products.objects.get(subcategory_id=id).annotate(mrp=F('selling_price')+300)
    
    page = Paginator(product,4)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    return render(request,"MshirtsP.html",{"product":page,"id_1":id})