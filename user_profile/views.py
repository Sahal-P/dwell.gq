from django.shortcuts import render,redirect
from accounts.models import Account, Address
from django.contrib.auth.views import PasswordChangeView , PasswordResetDoneView
from django.contrib import messages
# Create your views here.


def user_profile(request):
    try:
        user = request.user
        user_profile = Account.objects.get(email =user)
        address = Address.objects.filter(user = user)
        
        return render(request, 'profile.html' ,{"user_profile":user_profile,"address":address})
    except:
        messages.info(request, 'Please Login to view account detailes')
    return redirect(request.META.get('HTTP_REFERER'))

def edit_user_profile(request):
    user = request.user
    user_profile = Account.objects.get(email =user)
    
    if request.method =="POST":
        if request.POST['first_name']:
            first_name = request.POST.get('first_name')
            user_profile.first_name = first_name
            user_profile.save()
        if request.POST['last_name']:
            last_name = request.POST.get('last_name')
            user_profile.last_name = last_name
            user_profile.save()
        if request.POST['username']:
            username = request.POST.get('username')
            user_profile.username = username
            user_profile.save()
        if request.POST['email']:
            email = request.POST.get('email')
            user_profile.email = email
            user_profile.save()
        if request.POST['phone_number']:
            phone_number = request.POST.get('phone_number')
            user_profile.phone_number = phone_number
            user_profile.save()
        return redirect('user_profile')
        
    
    address = Address.objects.filter(user = user)
    return render(request, "edit_profile.html" ,{"user_profile":user_profile,"address":address})

def remove_address(request,id):
    destination = request.META.get('HTTP_REFERER')
    address = Address.objects.get(id=id)
    address.delete()
    
    return redirect(destination)

