from django.shortcuts import redirect, render, get_object_or_404
from .models import Products, Popularsearch
from .forms import *
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.http import require_POST
# Create your views here.

def index(request):
    products = Products.objects.order_by('-pk')
    search_all = Popularsearch.objects.order_by('-searchCount')[:3]
    context = {
        'products':products,
        'search_all': search_all,
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

@login_required
def delete(request, products_pk):
    products = get_object_or_404(Products, pk=products_pk)
    products.delete()
    return redirect('products:index')

@login_required
def zzi(request, products_pk):
    product = get_object_or_404(Products, pk=products_pk)
    if request.user in product.zzim.all():
        product.zzim.remove(request.user)
        user = product.user
        user.celsius -= 0.1
        user.celsius = round(user.celsius, 1)
        user.save()
    else:
        product.zzim.add(request.user)
        user = product.user
        user.celsius += 0.1
        user.celsius = round(user.celsius, 1)
        user.save()
    return redirect('products:detail', products_pk)

def sold_out(request, products_pk):
    product = get_object_or_404(Products, pk=products_pk)
    if request.user == product.user:
        if product.sold:
            product.sold = False
        else:
            product.sold = True
        product.save()
    return redirect('products:detail', products_pk)

# 검색 기능 + 검색어 저장
def search(request):
    search = request.GET.get("search")
    search_found = Popularsearch.objects.filter(terms=search)
    

    if search:
        # index에 검색 결과 뿌려주는 쿼리셋 저장
        search_result = Products.objects.filter(title__contains=search)
    
    # 사용자로부터 입력받은 검색어가 이미 있다면 searchCount += 1
    if search_found:
        search_exist = Popularsearch.objects.get(terms=search)
        search_exist.searchCount += 1
        search_exist.save()
    else:
        # 사용자로부터 입력받은 검색어를 DB에 저장
        Popularsearch.objects.create(terms=search)

    context = {
        'search_result': search_result,
    }
    return render(request, 'products/index.html', context)