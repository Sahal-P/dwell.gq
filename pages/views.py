from django.shortcuts import render,redirect
from django.utils.text import slugify
from accounts.models import Account
from category.models import Category, Products, SubCategory
from variation.models import Variation
from cart.models import GCart,CartItem
from django.db.models import Count,Sum,Q,F
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@never_cache
def index(request):
    return render (request,"index.html")

@never_cache
def shop(request):
    return render (request,"products.html")

@never_cache
def c_category(request):
    catag = Category.objects.all()
    return render (request,"category.html",{"catag":catag})

@never_cache
def mensSC(request,id):
    id = id
    subc= SubCategory.objects.filter(category_id = id)
    return render(request,"mensSC.html",{"subc":subc})

@never_cache
def MshirtsP(request,id):
    id = id
    product= Products.objects.filter(subcategory_id=id).annotate(mrp=F('selling_price')+300).order_by('id')
    
    for i in product:
        if i.category.discount<i.offer:
         if i.offer is not None and i.offer is not 0 :
            i.offer_price = int(i.original_price - i.original_price * i.offer/100)
            i.save()
            continue
        if i.category.discount is not None:
            i.category_offer = i.category.discount
            if i.category.discount is not 0:
                i.offer_price = int(i.original_price - i.original_price * i.category.discount/100)
            else:
                 i.offer_price = i.category.discount
            i.save()
    # product= Products.objects.get(subcategory_id=id).annotate(mrp=F('selling_price')+300)
    
    page = Paginator(product,4)
    page_list = request.GET.get('page')
    page = page.get_page(page_list)
    
    
    return render(request,"MshirtsP.html",{"product":page,"id_1":id})

@never_cache
def signle_P(request, id):
    id = id 
    obj = Products.objects.filter(id=id).annotate(mrp=F('selling_price')+300)
    # for i in obj:
    #     if i.offer is not None or i.category_offer is not None:
    #         i.offer_price = i.original_price - i.original_price * i.offer/100
    #         i.save()  
    variaiton1 = None
    variaiton2 = None
    prod = Products.objects.get(id=id)
    if Variation.objects.filter(product=prod).exists():
        variaiton1 = Variation.objects.filter(product=prod).values('color').distinct()
        variaiton2 = Variation.objects.filter(product=prod).values('size').distinct()
    return render (request, "product-single.html",{"obj":obj,"var":variaiton1,"var2":variaiton2,"id":id})

@never_cache
def productsingle(request):
    return render (request,"product-single.html")


def about(request):
    return render (request,"about.html")

def blog(request):
    return render (request,"blog.html")

def contact(request):
    return render (request,"contact.html")

@login_required(login_url='adminlogin')
def a_tables(request):
    person = Account.objects.all().order_by('id')
    return render(request, "admin/tables.html",{"person":person})


@login_required(login_url='adminlogin')
def category(request):
    cata = Category.objects.all()
    return render(request, "admin/category.html" ,{"cata":cata})

@login_required(login_url='adminlogin')
def subcategory(request):
    cata = SubCategory.objects.all()
    return render (request, "admin/subcategory.html",{"cata":cata})

@login_required(login_url='adminlogin')
def product(request):
    prod = Products.objects.all()
    return render (request, "admin/product.html", {"prod":prod})

@login_required(login_url='adminlogin')
def add_category(request):
    return render (request, "admin/add_category.html")

@login_required(login_url='adminlogin')
def add_subcategory(request):
    cata = Category.objects.all()
    return render (request, "admin/add_subcategory.html", {"cata":cata})

@login_required(login_url='adminlogin')
def add_product(request):
    catg = SubCategory.objects.all()
    Scata = Category.objects.all()
    return render (request, "admin/add_product.html" ,{"Scata":Scata})

@login_required(login_url='adminlogin')
def edit_subcategory(request, id):
    cata = Category.objects.all()
    subcategory =SubCategory.objects.get(id=id)
    if request.POST:
        subcategory =SubCategory.objects.get(id=id)
        if request.POST.get('category2'):
            cat1=request.POST.get('category2')
            subcategory.category_id = cat1
            subcategory.save()
        if request.POST['subcategory_name']:
            name = request.POST.get("subcategory_name")
            subcategory.subcategory_name = name
            subcategory.Sub_slug = slugify(name)
            subcategory.save()
        if request.FILES.get('img'):
            subcategory.Sub_img = request.FILES.get("img")
            subcategory.save()
        return redirect("pages:subcategory")
    return render (request, "admin/edit_subcategory.html", {"cata":cata,"subcategory":subcategory})

@login_required(login_url='adminlogin')
def edit_product(request,id):
    catg = SubCategory.objects.all()
    Scata = Category.objects.all()
    product = Products.objects.get(pk=id)
    if request.POST:
        product = Products.objects.get(pk=id)
        if request.POST['p_name']:
            name = request.POST.get("p_name")
            product.product_name=name
            product.slug=slugify(name)
            product.save()
        if request.POST['p_brand']:
            brand = request.POST.get("p_brand")
            product.brand=brand
            product.save()
        if request.POST['p_quantity']:
            quantity = request.POST.get("p_quantity")
            product.quantity=quantity
            product.save()
        if request.POST['p_og']:
            og = request.POST.get("p_og")
            product.original_price=og
            product.save()
        if request.POST['p_sp']:
            sp = request.POST.get("p_sp")
            product.selling_price=sp
            product.save()
        if request.POST.get('p_catg'):
            category = request.POST.get("p_catg")
            product.category_id =category
            product.save()
        if request.POST.get('p_scatg'):
            subcategory = request.POST.get("p_scatg")
            product.subcategory_id =subcategory
            product.save()
        if request.FILES.get('img1'):
            img1 = request.FILES.get("img1")
            product.product_img1 = img1
            product.save()
        if request.FILES.get('img2'):
            img2 = request.FILES.get("img2")
            product.product_img2 = img2
            product.save()
        if request.FILES.get('img3'):
            img3 = request.FILES.get("img3")
            product.product_img3 = img3 
            product.save()
        if request.FILES.get('img4'):
            img4 = request.FILES.get("img4")
            product.product_img4 = img4
            product.save()
        if request.POST['p_disc']:
            discription = request.POST.get("p_disc")
            product.description=discription
            product.save()
        if request.POST['p_av']:
            status = request.POST.get("p_av")
            product.status = status
            product.save()
        return redirect("pages:product")
    
    return render (request, "admin/edit_product.html",  {"catg":catg ,"Scata":Scata , "product":product })

@login_required(login_url='adminlogin')
def user_block(request):
    id= request.GET.get('id')
    val = request.GET.get('value')
    
    person = Account.objects.get(pk=id)
    if val =="True":
        person.is_blocked = True
        person.save()
    if val =="False":
        person.is_blocked = False
        person.save()
    return JsonResponse({"val":val})
