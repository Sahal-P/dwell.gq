from django.shortcuts import render,redirect
from orders.models import Orders,Products
from category.models import Offer_product, Category , Offer_category
from django.http import HttpResponse ,JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.


@login_required(login_url='adminlogin')
def product_offer(request):
    product = Products.objects.all()
    return render(request, 'admin/Product_offer.html',{'products':product})

@login_required(login_url='adminlogin')
def add_Product_offer(request,id):
    if request.POST:
        product = Products.objects.get(id = id)
        print(product)
        offer = Offer_product()
        Discount = request.POST.get('Discount')
        if Offer_product.objects.filter(product_id=id).exists():
            offer = Offer_product.objects.filter(product_id=id)
            for i in offer:
                i.product = product
                i.discount = Discount
                product.offer = Discount
                product.save()
                i.save()
            return redirect('product_offer')
        offer.discount = Discount
        offer.product = product
        offer.save()
        product.offer = Discount
        product.save()
        return redirect('product_offer')
    product = Products.objects.get(id=id)
    return render(request, "admin/add_Product_offer.html",{"product":product})

@login_required(login_url='adminlogin')
def category_offer(request):
    categorys = Category.objects.all()

    return render(request, 'admin/Category_offer.html',{"category":categorys})

@login_required(login_url='adminlogin')
def add_category_offer(request, id):
    if request.POST:
        category = Category.objects.get(id=id)
        Discount = request.POST.get('Discount')
        if Offer_category.objects.filter(category=category).exists():
            offer = Offer_category.objects.get(category=category)
            offer.discount = Discount   
            category.discount = Discount
            category.save()
            offer.save()
            return redirect('category_offer')
        else:
            offer = Offer_category()
            offer.category = category
            offer.discount = Discount
            offer.save()
            category.discount = Discount
            category.save()
            return redirect('category_offer')

    category = Category.objects.get(id = id)
    return render(request, 'admin/Add_category_offer.html',{"category":category})
   
@login_required(login_url='adminlogin')
def remove_category_offer(request):
    try:
        id = request.GET.get('id')
        category = Category.objects.get(id =id)
        discount = category.discount
        offer = Offer_category.objects.get(category = category)
        offer.discount = 0
        offer.save()
        # if Products.objects.filter(category=category,offer=discount).exists():
        prodects = Products.objects.filter(category=category,category_offer=discount)
        for i in prodects:
            i.category_offer =0
            i.save()
        category.discount = 0
        category.save()
        return JsonResponse({'id':id})
    except:
        return redirect('category_offer')

@login_required(login_url='adminlogin')
def remove_product_offer(request):
    id = request.GET.get('id')
    product = Products.objects.get(id =id)
    product.offer = 0
    product.offer_price = 0
    product.save()
    offer = Offer_product.objects.get(product_id=id)
    offer.discount =0
    offer.save()
    return JsonResponse({'id':id})
    
