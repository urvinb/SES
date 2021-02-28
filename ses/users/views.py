from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login


# Create your views here.
def signin(request):
    if request.user.is_authenticated:
        return redirect('index')

    if request.method == 'POST':
        username=request.POST.get("username")
        psw =request.POST.get("pass")
        user = authenticate(request, username=username, password=psw)
        if user is not None:
            login(request, user)
            return redirect('index')
        
        else:
            e = "Invalid username/password."
            return render(request,'users/login.html',{'e':e})

    return render(request,'users/login.html')


#Sign up 
def register(request,id,tab):
    if request.user.is_authenticated:
        return redirect('index')
        
    page = 1
    uname = ''
    if tab==2:
        page = 2

    if id!=0:
        us = User.objects.get(id=id)
        if uname:
            uname = us.username

    if 'next' in request.POST:
        username=request.POST.get("username")
        fname=request.POST.get("fname")
        lname=request.POST.get("lname")
        email=request.POST.get("email")
        psw =request.POST.get("pass")
        
        try:

            u = User.objects.create_user(email=email,password=psw,username=username)
            u.first_name = fname
            u.last_name = lname
            u.save()
            messages.success(request,f'You have successfully registered.')

            return redirect('signin')
        
        except:
            e='This username is already in use.Try again with a new one.'
            return render(request,'users/register.html',{'page':page,'e':e})

        
    return render(request,'users/register.html',{'page':page,'uname':uname})

def common(request):
    return render(request,'users/common.html')

def errorpage(request):
    return render(request,'users/errorpage.html')

