
from django.conf import settings
from twilio.rest import Client


import random


class otphandler:
    
    phone_number = None
    otp = None
    
    
    def __init__(self,phone_number , otp) -> None:
        
        self.phone_number= phone_number
        self.otp = otp
    def sent_otp_on_phone(self):
        sid_="AC85fdeaad04ced9b3d69c6db3cbea2621"
        token_="3410f8c9db89eecb7ece1a554c817aa4"
        client = Client(sid_,token_)

        message = client.messages.create(
                              body=f'YOUR OTP IS : {self.otp}',
                              from_='+13464832283',
                              to=self.phone_number
                          )

    