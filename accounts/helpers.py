from twilio.rest import Client
import random
from django.views.generic import View
from orders.models import Orders
from django.http import HttpResponse 
from . utils import *
from datetime import datetime, timedelta
from django.db.models import Count,Sum,Q,F
from django.conf import settings
class otphandler:
    phone_number = None
    otp = None
    sid_ = settings.SID_TWILIO
    token_ = settings.TOKEN_TWILIO
    def __init__(self,phone_number) -> None:
        self.phone_number= phone_number
        
    def sent_otp_on_phone(self):
        sid_= "AC85fdeaad04ced9b3d69c6db3cbea2621"
        token_= "03f12fd95abd9b10936f7e10778cf97a"
        client = Client(sid_,token_)
        otphandler.phone_number = self.phone_number
        otp = random.randint(1000, 9999)
        otphandler.Otp = str(otp)
        sent = "Dwell Shopping Account verification code is "+ str(otp)
        message = client.messages.create(
                              body=sent,
                              from_='+12136931880',
                              to='+91'+self.phone_number)
class signupgetuser:
    email = None
    def __init__(self,email) -> None:
        signupgetuser.email = email
        
        
        

def generatesalesReportPdf(request):

        to_date = request.GET.get('date' , '')
        from_date1 = to_date.split(",")[0]
        to_date1 = to_date.split(",")[1]
   
       
        t_date = datetime.strptime(to_date1 , "%Y-%m-%d")
        to_date11 = t_date + timedelta(1)
        
        print(from_date1,to_date11,"DDDDDDDDDDDDDDDDD")
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
