from twilio.rest import Client
import random
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.views.generic import View
from orders.models import Orders
from django.http import HttpResponse 
from . utils import *
import os
from datetime import datetime, timedelta
from django.db.models import Count,Sum,Q,F
from django.conf import settings

from django.contrib import messages
import smtplib, ssl
class otphandler:
    phone_number = None
    otp = None
   
    def __init__(self,phone_number) -> None:
        
        self.phone_number= phone_number
        
    def sent_otp_on_phone(self):
        sid_= getattr(settings, "SID_TWILIO", None)
        token_= getattr(settings, "TOKEN_TWILIO", None)
        client = Client(sid_,token_)
        
        otphandler.phone_number = self.phone_number
        # otp = random.randint(1000, 9999)
        # otphandler.Otp = str(otp)
        # sent = "Dwell Shopping Account verification code is "+ str(otp)
        # message = client.messages.create(
        #                       body=sent,
        #                       from_= getattr(settings, "TWILIO_PHONE", None),
        #                       to='+91'+self.phone_number)
        # account_sid = getattr(settings, "SID_TWILIO", None)
        # auth_token = getattr(settings, "TOKEN_TWILIO", None)
        # client = Client(account_sid, auth_token)
        verification = client.verify.v2.services('VA52f6fc8fa92fbcc412e330255536e6bf').verifications.create(to='+91'+self.phone_number, channel="sms")

        print(verification.status)
        
    def checkotp(self,otp):
        print('kkkkkk')
        sid_= getattr(settings, "SID_TWILIO", None)
        token_= getattr(settings, "TOKEN_TWILIO", None)
        client = Client(sid_,token_)
        print(self.phone_number,'phoooooooooo',otp)
        verification = client.verify.v2.services('VA52f6fc8fa92fbcc412e330255536e6bf').verification_checks.create(to='+91'+self.phone_number, code=otp)
        print(verification.status,"kkkkkkkkkk")
        
        if verification.status == "approved":
            return True
        else:
            return False
        
class signupgetuser:
    email = None
    phone_number = None
    def __init__(self,email,phone_number):
        self.email = email
        self.phone_number = phone_number
        
        
        

def generatesalesReportPdf(request):

        to_date = request.GET.get('date' , '')
        from_date1 = to_date.split(",")[0]
        to_date1 = to_date.split(",")[1]
        
        if to_date1 is '' or from_date1 is '':
            
            messages.info(request,"Please fill from and to date to export")
            return redirect(request.META.get('HTTP_REFERER')) 
       
        t_date = datetime.strptime(to_date1 , "%Y-%m-%d")
        to_date11 = t_date + timedelta(1)
        
        try:
            
           orders = Orders.objects.filter(orderd_date__range=[from_date1, to_date11]).annotate(sub_total=F('product__selling_price')*F('quantity'),margin_total=F('product__original_price')*F('quantity'),profit=(F('product__selling_price')-F('product__original_price'))*F('quantity')).order_by("-orderd_date")
           total_rev=0
           for i in orders:
               
               total_rev+=i.sub_total
           Report =[]

           for i in orders:
                   item={
                       'Date':i.orderd_date,
                       'User':i.user.first_name,
                       'Product':i.product.product_name,
                       'Quantity':i.quantity,
                       'Sell_price':i.product.selling_price,
                       'Profit':i.profit,
                       'Margin':i.margin_total,
                       'Revenue':i.sub_total,


                   },
                   Report.append(item)
                   
        except:
           return HttpResponse("505 not found")
        print(Report)
        values={
           'Report':Report,'fro':from_date1,'to':to_date1,'total_rev':total_rev,
        }
      
        format = render_to_pdf('admin/Report_pdf.html',values)
        return HttpResponse(format,content_type='application/pdf')



def GenerateInvoicePdf(request):
        
        id = request.GET.get('id')
        date_ = datetime.now()  
        try:
            
           data = Orders.objects.filter(order_id= id)
           Invoice =[]
           total_ = 0
           for i in data:
                   total_ += i.total_price
                   item={
                       'Date':i.orderd_date,
                       'User':i.user,
                        "Product": i.product,
                        "Quantity":i.quantity,
                        "Total":i.total_price,
                        "Address": i.address,
                   },
                   Invoice.append(item)
                   
                
        except:
           return HttpResponse("505 not found")
        values={'Invoice':Invoice,"total_":total_,"date_":date_}
        
        # return render(request,'Invoice_pdf.html',values)
        format = render_to_pdf('Invoice_pdf.html',values)
    
        return HttpResponse(format,content_type='application/pdf')

def GenerateCSV(request):
    
    
    return HttpResponse("csv")

            
