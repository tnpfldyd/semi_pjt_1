from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.contrib.auth import get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm , PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

def index(request):
    return render(request, 'accounts/index.html')

def signup(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        login(request, form.save())
        return redirect('articles:index')
    return render(request, 'accounts/signup.html', {'form': form})

def signin(request):
    form = AuthenticationForm() # 처음 들어오면 보이는 폼
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST) # 사용자가 입력한 내용
        if form.is_valid(): # 유효성 검사
            login(request, form.get_user())
            user = get_object_or_404(get_user_model(), pk=request.user.pk)
            if user.secession:
                logout(request)
                messages.error(request, '탈퇴 시 로그인은 불가능 합니다.😱')
                return redirect('accounts:login')
            return redirect('articles:index') # 통과하면 로그인 후에 articles/index로 리다이렉트
    context = {
        'form': form # 처음에 들어오면 method == 'GET' if문이 실행이 안되므로 18번째 줄 form을 반환,
                    # 만약 POST로 사용자가 입력한 내용이 유효성 검사를 통과 못하는 경우 20번째 줄 form을 반환
    }
    return render(request, 'accounts/login.html', context)

@login_required
def signout(request):
    logout(request)
    return redirect('articles:index')

def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    return render(request, 'accounts/profile.html', {'user': user})

@login_required
def follow(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if user != request.user:
        if user.followers.filter(pk=request.user.pk).exists():
            user.followers.remove(request.user)
            user.celsius -= 0.2
            user.celsius = round(user.celsius, 1)
            user.save()
        else:
            user.followers.add(request.user)
            user.celsius += 0.2
            user.celsius = round(user.celsius, 1)
            user.save()
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

@login_required
def editpw(request):
    form = PasswordChangeForm(request.user) # 처음 들어오면 보이는 폼
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST) # 사용자가 입력한 내용
        if form.is_valid(): # 유효성 검사
            form.save()
            update_session_auth_hash(request, form.user)
            return redirect('articles:index') # 통과하면 로그인 후에 리다이렉트
    context = {
        'form': form # 처음에 들어오면 method == 'GET' if문이 실행이 안되므로 18번째 줄 form을 반환,
                    # 만약 POST로 사용자가 입력한 내용이 유효성 검사를 통과 못하는 경우 20번째 줄 form을 반환
    }
    return render(request, 'accounts/editpw.html', context)

@login_required
def delete(request):
    form = CheckPasswordForm(request.user)
    if request.method == 'POST':
        form = CheckPasswordForm(request.user, request.POST)
        if form.is_valid():
            user = get_object_or_404(get_user_model(), pk=request.user.pk)
            user.secession = True
            user.save()
            logout(request)
            return redirect('articles:index')
    context = {
        'form': form,
    }
    return render(request, 'accounts/delete.html', context)

def question(request):
    return render(request, 'accounts/question.html')

@login_required
def block(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if user != request.user:
        if user.blockers.filter(pk=request.user.pk).exists():
            user.blockers.remove(request.user)
            user.celsius += 1
            user.celsius = round(user.celsius, 1)
            user.save()
        else:
            user.blockers.add(request.user)
            user.celsius -= 1
            user.celsius = round(user.celsius, 1)
            user.save()
    return redirect('accounts:profile', user.username)

@login_required
def block_user(request):
    block_users = request.user.blocking.all()
    return render(request, 'accounts/block_user.html', {'block_users': block_users})

@login_required
def block_user_block(request, pk):
    user = get_object_or_404(get_user_model(), pk=pk)
    if user != request.user:
        if user.blockers.filter(pk=request.user.pk).exists():
            user.blockers.remove(request.user)
            user.celsius += 1
            user.celsius = round(user.celsius, 1)
            user.save()
        else:
            user.blockers.add(request.user)
            user.celsius -= 1
            user.celsius = round(user.celsius, 1)
            user.save()
    return redirect('accounts:block_user')