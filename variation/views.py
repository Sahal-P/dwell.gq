from django.shortcuts import render
from . models import Products,Variation
from uuid import uuid4
from django.http import JsonResponse

def variation(request):
    id   = request.GET.get('id')
    prod = Products.objects.get(id = id)
    name = prod.product_name
    var = Variation.objects.filter(product=prod)
    return render(request, "admin/add_variation.html",{'name':name,"id":id ,"var":var})

def types(request):
    val = request.GET.get('varient')
    if val == 'color':
        types = ['red','green','black','white','yellow','blue','orange','brown','azure','gray','silver','purple']
    if val == 'size':
        types = ['small','medium','large','XL','XXL']
    return render(request, "admin/variation_types.html",{'types':types})

def addTypes(request):
    
    varient = request.GET.get('varient')
    id = request.GET.get('id')
    color = request.GET.get('type')
    price = request.GET.get('price')
    size = request.GET.get('size')
    quantity = request.GET.get('quantity')
    prod = Products.objects.get(id = id)
    v_id= str(uuid4())[:6]
    variation_id = str(prod.product_id)+v_id
    print(variation_id,"<<<<<<,")
    create = Variation.objects.create(product=prod,size=size,quantity=quantity,color=color,variation_id=variation_id,price=price)
    create.save()
    var = Variation.objects.filter(product=prod)

    return render(request, "admin/variation_table.html" ,{"var":var})



def check_variation(request):
    color = request.GET.get('color')
    size = request.GET.get('size')
    print(color,size,"LLLLLLLLLLLLLL")
    try:
        v = Variation.objects.get(color=color,size=size)
        print(v)
        status = True
        price = v.price
        return JsonResponse({"status":status,"price":price})
    except Variation.DoesNotExist:
        status = False
        return JsonResponse({"status":status})
        
    