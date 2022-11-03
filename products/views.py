from django.shortcuts import redirect, render, get_object_or_404
from .models import Products
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST
# Create your views here.

def index(request):
    products = Products.objects.order_by('-pk')
    context = {
        'products':products,
    }
    return render(request, 'products/index.html', context)

@login_required
def create(request):
    productform = ProductsForm()
    locationform = LocationForm()
    if request.method == "POST":
        productform = ProductsForm(request.POST, request.FILES)
        locationform = LocationForm(request.POST)
        print(locationform)
        if productform.is_valid() and locationform.is_valid(): # 유효성 검사
            # 로그인한 유저만 글 작성가능해서
            products = productform.save(commit=False)
            products.user = request.user
            products.save()
            location = locationform.save(commit=False)
            location.product = products
            location.save()
            # 일단 임의로 redirect
            return redirect('products:index')
    context = {
        'productform':productform,
        'locationform':locationform,
    }
    return render(request, 'products/form.html', context)

def detail(request, products_pk):
    products = get_object_or_404(Products, pk=products_pk)
    location = get_object_or_404(Location, product_id=products_pk)
    products.hit += 1
    products.save()
    context = {
        'products':products,
        'location':location,
    }
    return render(request,'products/detail.html', context)

@login_required
def update(request, products_pk):
    products = get_object_or_404(Products, pk=products_pk)
    loca = get_object_or_404(Location, product_id=products_pk)
    # 로그인한 유저와 작성한 유저가 같다면
    if request.user == products.user:
        if request.method == "POST":
            form = ProductsForm(request.POST, request.FILES, instance=products)
            locationform = LocationForm(request.POST, instance=loca)
            if form.is_valid():
                # 로그인 구현을 아직 안해서
                form.save()
                locationform.save()
                return redirect('products:detail', products.pk)
        else:
            form = ProductsForm(instance=products)
            locationform = LocationForm(instance=loca)
        context = {
            'productform':form,
            'locationform' : locationform,
        }
        return render(request, 'products/form.html', context)
    # 작성자가 아닐 때
    else:
        return redirect('products:detail', products.pk)

def delete(request, products_pk):
    products = get_object_or_404(Products, pk=products_pk)
    products.delete()
    return redirect('products:index')
