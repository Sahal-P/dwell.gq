from django.conf import settings
from twilio.rest import Client
import random

class otphandler:
    phone_number = None
    otp = None
    
    def __init__(self,phone_number) -> None:
        self.phone_number= phone_number
        
    def sent_otp_on_phone(self):
        sid_="AC85fdeaad04ced9b3d69c6db3cbea2621"
        token_="f09e612351f6f8142642715e1818b453"
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