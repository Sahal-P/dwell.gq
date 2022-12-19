from django.shortcuts import render, redirect
from . models import Coupens
from django.contrib import messages
from django.http import HttpResponse
from cart.models import CartItem
import datetime
from django.contrib.auth.decorators import login_required

@login_required(login_url='adminlogin')
def add_coupen(request):
    if request.POST:
        if not request.POST.get('coupen_code'):
            messages.error(request,'Coupen code is required')
            return redirect('coupen')
        code        = request.POST.get('coupen_code')
        discount    = request.POST.get('coupen_discount')
        validity    = request.POST.get('coupen_validity')
        limit       = request.POST.get('coupen_limit')
        coupen      = Coupens.objects.create(coupen_code=code, coupen_limit = limit, validity_upto = validity, discount=discount)
        coupen.save()
        messages.success(request,'Coupen added succesfully')
        return redirect('coupen')

@login_required(login_url='adminlogin')
def coupen(request):
    coupen      = Coupens.objects.all()
    return render(request, "admin/Add_coupen.html", {"coupen":coupen})


def Applay_coupen(request):
    
    if request.POST:
        # user = request.user
        d = datetime.datetime.today()
        now =datetime.date(d.year, d.month, d.day)
      
        # cart_items = CartItem.objects.filter(user = user,is_active=True)
        total = request.POST.get('total')
        total = float(total)
        code = request.POST.get('coupen_code')
        try:
            coupen = Coupens.objects.get(coupen_code = code)
        except:
            messages.error(request,"Please enter a valid Coupen")
            return redirect(request.META.get('HTTP_REFERER'))
        if coupen.is_active == False :
            messages.error(request,"The coupen is invalid")
            return redirect(request.META.get('HTTP_REFERER'))
        if coupen.validity_upto < now:
            messages.error(request,"Sorry The coupen is expired")
            return redirect(request.META.get('HTTP_REFERER'))
        if coupen.is_used :
            messages.error(request,"This coupen is alreday used")
            return redirect(request.META.get('HTTP_REFERER'))
        if code == coupen.coupen_code:
            
            discount = coupen.discount
            limit = coupen.coupen_limit
            limited_price = total - limit
            discounted_price = total - total*discount/100
            if limited_price > discounted_price:
                new_price = limited_price
            else:
                new_price = discounted_price
            coupen.is_used = True
            coupen.save()
            request.session['new_price'] = new_price
            request.session['coupen'] = code
            return redirect(request.META.get('HTTP_REFERER'))
            
            
    return HttpResponse('True')



def remove_coupen(request):
    
    code = request.session['coupen']
    coupen = Coupens.objects.get(coupen_code = code)
    coupen.is_used = False
    coupen.save()
    request.session.pop('coupen',None)
    request.session.pop('new_price',None)
    request.session.modified = True
    
    return redirect(request.META.get('HTTP_REFERER')) 