from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm , PasswordChangeForm
from django.contrib.auth.decorators import login_required
# Create your views here.

def index(request):
    return render(request, 'accounts/index.html')

def signup(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        return redirect('accounts:index')
    return render(request, 'accounts/signup.html', {'form': form})

def signin(request):
    form = AuthenticationForm() # 처음 들어오면 보이는 폼
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) # 사용자가 입력한 내용
        if form.is_valid(): # 유효성 검사
            login(request, form.get_user())
            return redirect('accounts:index') # 통과하면 로그인 후에 리다이렉트
    context = {
        'form': form # 처음에 들어오면 method == 'GET' if문이 실행이 안되므로 18번째 줄 form을 반환,
                    # 만약 POST로 사용자가 입력한 내용이 유효성 검사를 통과 못하는 경우 20번째 줄 form을 반환
    }
    return render(request, 'accounts/login.html', context)

@login_required
def signout(request):
    logout(request)
    return redirect('accounts:index')

def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    return render(request, 'accounts/profile.html', {'user': user})

@login_required
def follow(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if user != request.user:
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
        else:
            user.followers.add(request.user)
    return redirect('accounts:profile', user.username)

@login_required
def edit(request):
    if request.method == "POST":
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if user_change_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
            return redirect("accounts:profile", user.username)
        return redirect("accounts:edit")
    user_change_form = CustomUserChangeForm(instance=request.user)
    pro, create = Profile.objects.get_or_create(user=request.user)
    profile_form = ProfileForm(instance=pro)
    context = {
        "user_change_form": user_change_form,
        "profile_form": profile_form,
    }
    return render(request, "accounts/edit.html", context)

def editpw(request):
    form = PasswordChangeForm(request.user) # 처음 들어오면 보이는 폼
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST) # 사용자가 입력한 내용
        if form.is_valid(): # 유효성 검사
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('accounts:index') # 통과하면 로그인 후에 리다이렉트
    context = {
        'form': form # 처음에 들어오면 method == 'GET' if문이 실행이 안되므로 18번째 줄 form을 반환,
                    # 만약 POST로 사용자가 입력한 내용이 유효성 검사를 통과 못하는 경우 20번째 줄 form을 반환
    }
    return render(request, 'accounts/editpw.html', context)

def delete(request):
    form = CheckPasswordForm(request.user)
    if request.method == 'POST':
        form = CheckPasswordForm(request.user, request.POST)
        if form.is_valid():
            request.user.delete()
            logout(request)
            return redirect('accounts:index')
    context = {
        'form': form,
    }
    return render(request, 'accounts/delete.html', context)