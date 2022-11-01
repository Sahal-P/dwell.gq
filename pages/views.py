from django.shortcuts import render,redirect
from django.utils.text import slugify


from accounts.models import Account
from category.models import Category, Products, SubCategory

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



def cart(request):
    return render (request,"cart.html")



def checkout(request):
    return render (request,"checkout.html")



def about(request):
    return render (request,"about.html")



def blog(request):
    return render (request,"blog.html")




def contact(request):
    return render (request,"contact.html")



def a_tables(request):
    person = Account.objects.all()
    return render(request, "admin/tables2.html",{"person":person})



def a_tables2(request):
    person = Account.objects.all()
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
    return render (request, "admin/add_product.html", {"catg":catg ,"Scata":Scata })


def edit_subcategory(request, id):
    cata = Category.objects.all()
    if request.POST:
        subcategory =SubCategory.objects.get(id=id)
        print(request.POST.get('category2'))
        cat1=request.POST.get('category2')
        print(cat1,"<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
        name = request.POST.get("subcategory_name")
        
        subcategory.Sub_img = request.FILES["img"]
        subcategory.subcategory_name = name
        subcategory.Sub_slug = slugify(name)
        
        subcategory.category_id = cat1
        
        subcategory.save()
        
        return redirect("pages:subcategory")
    
    return render (request, "admin/edit_subcategory.html", {"cata":cata})