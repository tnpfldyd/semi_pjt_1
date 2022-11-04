from django.shortcuts import render, redirect, get_object_or_404
from .forms import ServiceCenterForm, CommentForm
from .models import ServiceCenter, ServiceComment
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'service_center/index.html')

@login_required
def question(request):
    if request.method == "POST":
        service_form = ServiceCenterForm(request.POST,request.FILES)
        if service_form.is_valid():
            service = service_form.save(commit=False)
            service.user = request.user
            service.save()
            return redirect(request.GET.get("next") or 'service_center:index')
    else:
        service_form = ServiceCenterForm()
    context = {
        'service_form':service_form,
    }
            
    return render(request, 'service_center/question.html', context)

@login_required
def detail(request, service_pk):
    question = get_object_or_404(ServiceCenter, pk=service_pk)
    comment_form = CommentForm()
    context = {
        'question':question,
        'comment_form':comment_form,
        'comments':question.center.all(),
    }
    return render(request, 'service_center/detail.html', context)

def comment_create(request, service_pk):
    question = get_object_or_404(ServiceCenter, pk=service_pk)
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.service = question
        comment.user = question.user
        comment.save()
    return redirect('service_center:detail', question.pk)