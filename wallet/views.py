from django.shortcuts import render
from .models import Wallet
from accounts.models import Account,ReferalSection

# Create your views here.
def wallet(request):
    user = request.user
    wallet = Wallet.objects.get(user_id=user)
    
    return render(request, "wallet.html",{"wallet":wallet})