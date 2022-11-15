from distutils.log import error
from email import message
from django.shortcuts import render, redirect
from .models import *
# Create your views here.
from django.utils.text import slugify




def add_category(request):
    if request.POST:
        name = request.POST.get("category_name")
        category = Category()
        if Category.objects.filter(category_name=name).exists():
            message.error(request,"catagory already exists")
            return redirect ("pages:add_category")
        if 'img' in request.FILES:
            category.cata_img = request.FILES['img']
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
            category.category_name = name
            category.slug = slugify(name)
            category.save()
        if 'img' in request.FILES:
            category.cata_img = request.FILES['img']
            category.save()
        return redirect('pages:category')
    return render(request, "admin/edit_category.html" )

def delete_category(request,id):
        category = Category.objects.get(pk=id)
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
        img1 = request.FILES["img1"]
        img2 = request.FILES["img2"]
        img3 = request.FILES["img3"]
        img4 = request.FILES["img4"]
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
        product.product_img2 = img2 
        product.product_img3 = img3 
        product.product_img4 = img4
        product.status = status
        product.category_id =category
        product.subcategory_id =subcategory
        product.save()
        return redirect("pages:product")
    return render (request, "admin/add_product.html")

def delete_subcategory(request,id):
        subcategory = SubCategory.objects.get(pk=id)
        subcategory.delete()
        return redirect("pages:subcategory")
    
def delete_product(request, id ):
    product = Products.objects.get(pk=id)
    product.delete()
    return redirect ("pages:product")

def dropdown_P(request):
    category = request.GET.get("category")
    subcat1 = SubCategory.objects.filter(category_id=category).all()
    return render(request, "admin/P_dropdown.html",{"subcat1":subcat1})

def dropdown_PE(request):
    category = request.GET.get("category")
    subcat = SubCategory.objects.filter(category_id=category).all()
    return render(request, "admin/PE_dropdown copy.html",{"subcat":subcat})



