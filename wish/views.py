from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required

from .models import *
# Create your views here.

def signup_view( request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if User.objects.filter(email = email).exists():
            messages.error(request, 'Account with email exists')
        elif len(password1) < 8:
            messages.error(request,'Password too short \nIt should be atleast 8 characters')
        elif password1 == password2:
            user = User(email = email, password = make_password(password1), username =  username)
            user.save()
            return redirect('login')
        else:
            messages.error(request,'Passwords don\'t match ')
    return render(request, 'signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email = email, password = password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else: 
            messages.error(request,'Passwords don\'t match')
        
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

@login_required(login_url='login')
def add_item(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        item = Wish(name = name, description = description, user = request.user, image = image)
        item.save()
        return redirect('home')
    return render(request, 'additem.html')

@login_required(login_url='login')
def edit_item(request, pk):
    item = Wish.objects.get(id = pk)
    if request.method == 'POST' and request.user == item.user:
        item.name = request.POST.get('name')
        item.description = request.POST.get('description')
        if request.FILES.get('image'):
            item.image = request.FILES.get('image')
        item.save()
        return redirect('home')
    
    context = {'item': item}
    return render(request,  'additem.html', context)

@login_required(login_url='login')
def delete_item(request,pk):
     item = Wish.objects.get(id = pk)
     item.delete()
     path = request.META.get('HTTP_REFERER')
     return redirect(path)

def home(request):
    user = request.user
    domain = request.get_host()
    link = f'{domain}/'
    wishes = Wish.objects.filter(user__id = user.id)
    context = {'link':link, 'wishes':wishes, 'user':user}
    return render(request, 'home.html', context)

def wishes(request, username):
    try:
        user = User.objects.get(username = username)
    except:
        return HttpResponse('Page Not Found')
    domain = request.get_host()
    link = f'{domain}/'
    wishes = Wish.objects.filter(user__id = user.id)
    context = {'link':link, 'wishes':wishes, 'user':user}
    return render(request, 'wishes.html', context)  



            


