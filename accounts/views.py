from cProfile import Profile
import email
from email import message
from pyexpat.errors import messages
from urllib import request
from urllib.request import Request
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
# Create your views here.
from .helpers import *
from .models import Account , profile

def d_admin(request):
    if request.user.is_authenticated:
        
       return render(request, "admin/index.html")
    return redirect("adminlogin")
def home(request):
    if request.user.is_authenticated:
        return render(request, "index.html")
    
    else:
      return render(request, "login.html")

def user_login(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.POST:
        email = request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request, email=email,password=password)
        
        if user is not None:
            login(request,user)
            return redirect("home")
    return render(request,"login.html")

def user_signup(request,*args, **kwargs):
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        first_name= request.POST.get("first_name")
        last_name= request.POST.get("last_name")
        email = request.POST.get("email")
        phone_number = request.POST.get("phone_number")
        username = request.POST.get("username")
        password = request.POST.get("password1")
        if Account.objects.filter(username=username).exists():
            messages.error(request,'username is already exist')
            
            return redirect ('user_signup')
        if Account.objects.filter(email=email).exists():
            message.error(request, 'email is already exist')
            return redirect ('user_signup')
        user = Account.objects.create_user(first_name=first_name,last_name=last_name,email=email,username= username,phone_number=phone_number,password=password)
        
        user.save()
        print(user)
       
        user1 = authenticate(request,email=email,password=password)
        
        print(user1,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        if user1 is not None:
         login(request,user1)   
         return redirect("home")
  
  
    return render(request,"signup.html")
         

        
        
def log_out(request):
    logout(request)
    return render(request, "login.html")



     
def user_otp(request):
    if request.user.is_authenticated:
        return redirect("home")
    if request.POST:
        
        phone_number = request.POST.get("phone_number")
        
        phone=Account.objects.filter(phone_number=phone_number).exists()
        
        print(phone,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        print(phone_number)
        
        if phone is True:
            user = Account.objects.get(phone_number=phone_number)
            
            request.user = user
            print(request.user,"<<<<<<<<<<")
            otp = random.randint(1000,9999)
            T= profile.objects.create(otp=otp)
            
            otp_handler = otphandler('+91'+phone_number,otp).sent_otp_on_phone()
            
            login(request,user)
            
            return redirect("otp_v")
    
    return render(request,'otp.html')


def otp_v(request):
    print(request.user  ,'<<<<<<<<<<<<<<<<<<<<<<<<')
    user =request.user
    if request.method == "POST":
        otp1 = request.POST.get("otp1")
        otp2 = request.POST.get("otp2")
        otp3 = request.POST.get("otp3")
        otp4 = request.POST.get("otp4")
        otp5 = otp1+otp2+otp3+otp4
        
        print(otp5)
        
        if profile.objects.filter(otp=otp5):
            login(request,user)
            
            return render(request,"index.html")
    
    
    return render (request, "otpv.html")


def adminlogin(request):
    if request.POST:
        print("<<<<<<<<<<<")
        email= request.POST.get("email")
        password = request.POST.get("password")
        
        user = authenticate(request,email=email,password=password)
        print(user)
        if user is not None:
            if user.is_superuser is True:
               print("<<<<<<<<<")
               login(request,user)
               return redirect("d_admin")
    return render (request, "admin/login.html")

def adminlogout(request):
    logout(request)
    return redirect(adminlogin)