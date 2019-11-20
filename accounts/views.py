from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from .forms import CustomUserCreationForm
from .models import User
# Create your views here.


def userlist(request):
    users = User.objects.all()

    context = {
        'users': users
    }
    return render(request, 'accounts/userlist.html', context)


def userpage(request, id):
    user_info = get_object_or_404(User, id=id)
    context = {
        'user_info': user_info
    }
    return render(request, 'accounts/userpage.html', context)


def signup(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


def login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('movies:index')
    else:
        form = AuthenticationForm()
    context = {
        'form': form
    }
    return render(request, 'accounts/form.html', context)


def logout(request):
    auth_logout(request)
    return redirect("accounts:login")


def follow(request, id):
    you = get_object_or_404(User, id=id)
    me = request.user

    if me.is_authenticated and you != me:
        if you.followers.filter(id=me.id):
            you.followers.remove(me)
        else:
            you.followers.add(me)
    return redirect('accounts:userpage', id)
