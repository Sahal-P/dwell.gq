from distutils.log import error
from django.shortcuts import render, redirect
from .models import *
# Create your views here.
from django.utils.text import slugify
from django.conf import settings
import os
from django.contrib import messages
from django.http import JsonResponse
from uuid import uuid4



def add_category(request):
    if request.POST:
        name = request.POST.get("category_name")
        if not name:
            messages.error(request,"category needs a name")
            return redirect(request.META.get('HTTP_REFERER'))
        category = Category()
        if Category.objects.filter(category_name=name).exists():
            messages.error(request,"catagory already exists , please choose a diffrent name")
            return redirect(request.META.get('HTTP_REFERER'))
        image = request.FILES.get('img')
        if not image:
            messages.error(request,"category needs an Image")
            return redirect(request.META.get('HTTP_REFERER'))
        category.cata_img = image
        category.category_name = name
        category.slug= slugify(name)
        category.save()
        # message.error(request,"new category added")
        return redirect('pages:category')
    return render (request, "admin/add_category.html")

def edit_category(request,id):
    
    if request.POST:
        category =Category.objects.get(pk=id)
        if request.POST['category_name']:
            name = request.POST.get("category_name")
            if Category.objects.filter(category_name=name).exists():
                messages.error(request,"catagory already exists , please choose a diffrent name")
                return redirect(request.META.get('HTTP_REFERER'))
            category.category_name = name
            category.slug = slugify(name)
            category.save()
        image = request.FILES.get('img')
        if image is not None:
            category.cata_img = image
        category.save()
        return redirect('pages:category')
    return render(request, "admin/edit_category.html" )

def delete_category(request,id):
        category = Category.objects.get(pk=id)
        img_path=category.cata_img
        prod_img_path = Products.objects.filter(category_id=id)
    
        for i in prod_img_path:
            if i.product_img1:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i.product_img1)))
            if i.product_img2:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i.product_img2)))
            if i.product_img3:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i.product_img3)))
            if i.product_img4:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i.product_img4)))
                
        sub_img = SubCategory.objects.filter(category_id=id)
        for i in sub_img:
            os.remove(os.path.join(settings.MEDIA_ROOT, str(i.Sub_img)))
        os.remove(os.path.join(settings.MEDIA_ROOT, str(img_path)))
        category.delete()
        return redirect("pages:category")
        
def add_subcategory(request):
    if request.POST:
        subcategory= SubCategory()
        print(request.POST.get('category'))
        cat1=request.POST.get('category')
        name = request.POST.get("subcategory_name")
        subcategory.Sub_img = request.FILES["img"]
        subcategory.subcategory_name = name
        subcategory.Sub_slug = slugify(name)
        subcategory.category_id = cat1
        subcategory.save()
        return redirect("pages:subcategory")
    return render(request , "admin/add_subcategory.html")

def add_product(request):
    if request.POST:
        product = Products()
        name = request.POST.get("p_name")
        brand = request.POST.get("p_brand")
        quantity = request.POST.get("p_quantity")
        og = request.POST.get("p_og")
        sp = request.POST.get("p_sp")
        category = request.POST.get("p_catg")
        subcategory = request.POST.get("p_scatg")
        img1 = request.FILES.get("img1")
        if request.FILES.get("img2") is not None:
            img2 = request.FILES.get("img2")
            product.product_img2 = img2 
        if request.FILES.get("img3") is not None:
            img3 = request.FILES.get("img3")
            product.product_img3 = img3 
        if request.FILES.get("img4") is not None:
            img4 = request.FILES.get("img4")
            product.product_img4 = img4
        discription = request.POST.get("p_disc")
        status = request.POST.get("p_av")
        product.product_name=name
        product.slug=slugify(name)
        product.brand=brand
        product.description=discription
        product.quantity=quantity
        product.original_price=og
        product.selling_price=sp
        product.product_img1 = img1 
        product.status = status
        product.category_id =category
        product.subcategory_id =subcategory
        product.product_id = str(uuid4())[:12]
        product.save()
        return redirect("pages:product")
    return render (request, "admin/add_product.html")

def delete_subcategory(request,id):
        subcategory = SubCategory.objects.get(pk=id)
        prod_img = Products.objects.filter(subcategory_id = id)
        for i in prod_img:
            if i.product_img1:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i.product_img1)))
            if i.product_img2:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i.product_img2)))
            if i.product_img3:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i.product_img3)))
            if i.product_img4:
                os.remove(os.path.join(settings.MEDIA_ROOT, str(i.product_img4)))
        img_path = subcategory.Sub_img
        os.remove(os.path.join(settings.MEDIA_ROOT, str(img_path)))
        subcategory.delete()
        return redirect("pages:subcategory")
    
def delete_product(request):
    id = request.GET.get('id')
    product = Products.objects.get(pk=id)
    
    if product.product_img1:
        os.remove(os.path.join(settings.MEDIA_ROOT, str(product.product_img1)))
    if product.product_img2:
        os.remove(os.path.join(settings.MEDIA_ROOT, str(product.product_img2)))
    if product.product_img3:
        os.remove(os.path.join(settings.MEDIA_ROOT, str(product.product_img3)))
    if product.product_img4:
        os.remove(os.path.join(settings.MEDIA_ROOT, str(product.product_img4)))
    product.delete()
    return JsonResponse({"id":id})

def dropdown_P(request):
    category = request.GET.get("category")
    subcat1 = SubCategory.objects.filter(category_id=category).all()
    return render(request, "admin/P_dropdown.html",{"subcat1":subcat1})

def dropdown_PE(request):
    category = request.GET.get("category")
    subcat = SubCategory.objects.filter(category_id=category).all()
    return render(request, "admin/PE_dropdown copy.html",{"subcat":subcat})



