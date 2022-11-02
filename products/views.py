from django.shortcuts import redirect, render, get_object_or_404
from .models import Products, Location
from .forms import ProductsForm
from django.contrib.auth.decorators import login_required
from accounts.models import User
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
    if request.method == "POST":
        form = ProductsForm(request.POST, request.FILES)
        
        if form.is_valid(): # 유효성 검사
            # 로그인한 유저만 글 작성가능해서
            products = form.save(commit=False)
            products.user = request.user
            form.save()
            # 일단 임의로 redirect
            return redirect('products:index')
    else:
        form = ProductsForm()
    context = {
        'form':form,
    }
    return render(request, 'products/form.html', context)

def detail(request, products_pk):
    products = get_object_or_404(Products, pk=products_pk)
    context = {
        'products':products,
    }
    return render(request,'products/detail.html', context)

@login_required
def update(request, products_pk):
    products = get_object_or_404(Products, pk=products_pk)
    # 로그인한 유저와 작성한 유저가 같다면
    if request.user == products.user:
        if request.method == "POST":
            form = ProductsForm(request.POST, request.FILES, instance=products)
            if form.is_valid():
                # 로그인 구현을 아직 안해서
                form.save(commit=False)
                products.user = request.user
                form.save()
                return redirect('products:detail', products.pk)
        else:
            form = ProductsForm(instance=products)
        context = {
            'form':form,
        }
        return render(request, 'products/form.html', context)
    # 작성자가 아닐 때
    else:
        return redirect('products:detail', products.pk)

def delete(request, products_pk):
    products = get_object_or_404(Products, pk=products_pk)
    products.delete()
    return redirect('products:index')

# location
@require_POST
def location(request):
    if request.method == "POST":
        location = Location()
        location.input_lat = request.POST['lat']
        location.input_lon = request.POST['lon']
        location.save()
        print(location.input_lat)
        # json 형식으로 응답
        return HttpResponse(content_type='application/json')