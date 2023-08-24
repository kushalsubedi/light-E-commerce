from django.shortcuts import render,redirect,get_object_or_404,HttpResponse
from django.http import HttpResponseNotFound

from .forms import ProductForm,CategoryForm
from .models import Product,category,CartItem

from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def home(request):
 


    product=Product.objects.all()

    return render(request,'Home/index.html',{'product':product})


def create_category(request):
    if not request.user.is_staff:
        return HttpResponse("Page not Found")
    if request.method=='POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
    form = CategoryForm(request.POST)
    context={'form':form}
    return render(request,'Home/create_category.html',context)

@login_required
def create_Product(request):
    if not request.user.is_staff:
        return  HttpResponseNotFound("Page not found")

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product= form.save(commit=False)
            product.author = request.user
            product.save()
            print(form.cleaned_data)
            return redirect('product_detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request,'Home/create.html',{'form':form})

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'Home/product_detail.html', {'product': product})

@login_required
def update_product(request,pk):
    if request.user == get_object_or_404(Product,pk=pk).author: 
        # or you can Do this if request.user == Product.objects.get(pk=pk).author:
        product=get_object_or_404(Product,pk=pk)
        form=ProductForm(instance=product)
   
        if request.method == 'POST':
            form=ProductForm(request.POST,request.FILES,instance=product)
            if form.is_valid():
                form.save()
                return redirect('product_detail',pk=product.pk)
            else:
                print(form.errors)
            
        context={'form':form}
    
        return render(request,'Home/create.html',context)
    else :
        return HttpResponse("<h1> You are not allowed to edit this product </h1>",status=403)
    
@login_required
def delete_product(request,pk):
    if request.user == Product.objects.get(pk=pk).author:
        product=Product.objects.get(pk=pk)
        product.delete()
        return redirect('home')
    else :
        return HttpResponse("<h1> You are not allowed to delete this product </h1>",status=403)


# def cart_view(request, product_id):
#     product = Product.objects.get(id=product_id)

#     if request.method == "POST":
#         quantity = int(request.POST["quantity"])
#         cart_item, created = CartItem.objects.get_or_create(product=product)
#         cart_item.quantity = quantity
#         cart_item.save()

#         return redirect("cart")

#     cart_items = CartItem.objects.filter(user=request.user)
#     return render(request, "cart.html", {"cart_items": cart_items})



