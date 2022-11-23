from django.shortcuts import render,redirect
from django.utils.text import slugify
from accounts.models import Account
from category.models import Category, Products, SubCategory
from cart.models import Cart,CartItem

# Create your views here.

def index(request):
    return render (request,"index.html")

def shop(request):
    return render (request,"products.html")

def c_category(request):
    catag = Category.objects.all()
    return render (request,"category.html",{"catag":catag})

def mensSC(request,id):
    id = id
    subc= SubCategory.objects.filter(category_id = id)
    return render(request,"mensSC.html",{"subc":subc})

def MshirtsP(request,id):
    id = id
    product= Products.objects.filter(subcategory_id=id)
    return render(request,"MshirtsP.html",{"product":product})

def signle_P(request, id):
    id = id 
    obj = Products.objects.filter(id=id)
    return render (request, "product-single.html",{"obj":obj})

def productsingle(request):
    return render (request,"product-single.html")

def about(request):
    return render (request,"about.html")

def blog(request):
    return render (request,"blog.html")

def contact(request):
    return render (request,"contact.html")

def a_tables(request):
    person = Account.objects.all().order_by('id')
    return render(request, "admin/tables.html",{"person":person})



def category(request):
    cata = Category.objects.all()
    return render(request, "admin/category.html" ,{"cata":cata})

def subcategory(request):
    cata = SubCategory.objects.all()
    return render (request, "admin/subcategory.html",{"cata":cata})

def product(request):
    prod = Products.objects.all()
    return render (request, "admin/product.html", {"prod":prod})

def add_category(request):
    return render (request, "admin/add_category.html")

def add_subcategory(request):
    cata = Category.objects.all()
    return render (request, "admin/add_subcategory.html", {"cata":cata})

def add_product(request):
    catg = SubCategory.objects.all()
    Scata = Category.objects.all()
    return render (request, "admin/add_product.html" ,{"Scata":Scata})

def edit_subcategory(request, id):
    cata = Category.objects.all()
    if request.POST:
        subcategory =SubCategory.objects.get(id=id)
        cat1=request.POST.get('category2')
        subcategory.category_id = cat1
        subcategory.save()
        if request.POST['subcategory_name']:
            name = request.POST.get("subcategory_name")
            subcategory.subcategory_name = name
            subcategory.Sub_slug = slugify(name)
            subcategory.save()
        if request.POST['img']:
            subcategory.Sub_img = request.FILES["img"]
            subcategory.save()
        return redirect("pages:subcategory")
    return render (request, "admin/edit_subcategory.html", {"cata":cata})

def edit_product(request,id):
    catg = SubCategory.objects.all()
    Scata = Category.objects.all()
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
        if request.POST['p_catg']:
            category = request.POST.get("p_catg")
            product.category_id =category
            product.save()
        if request.POST['p_scatg']:
            subcategory = request.POST.get("p_scatg")
            product.subcategory_id =subcategory
            product.save()
        if request.POST['img1']:
            img1 = request.FILES["img1"]
            product.product_img1 = img1
            product.save()
        if request.POST['img2']:
            img2 = request.FILES["img2"]
            product.product_img2 = img2
            product.save()
        if request.POST['img3']:
            img3 = request.FILES["img3"]
            product.product_img3 = img3 
            product.save()
        if request.POST['img4']:
            img4 = request.FILES["img4"]
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
    
    return render (request, "admin/edit_product.html",  {"catg":catg ,"Scata":Scata })

def user_block(request, id):
    id=id
    val = request.GET.get('bl')
    val2 = request.GET.get('ubl')
    person = Account.objects.get(pk=id)
    if val is not None:
        person.is_blocked = True
        person.save()
    if val2 is not None:
        person.is_blocked = False
        person.save()
    return redirect('pages:a_tables')
