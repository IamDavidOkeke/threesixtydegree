from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.urls import reverse

# Create your views here.

def home(request):
    return render(request, 'home.html', {})


def register(request):
    if request.method == 'POST':
        user = User.objects.create_user(
          request.POST['username'],
          request.POST['email'],
          request.POST['password']
        )
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        return HttpResponseRedirect('/login/')
    else:
        return render(request, 'register.html', {})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in")
            return HttpResponseRedirect(reverse('profile'))
        else: 
            messages.success(request, "Error logging in, Please try again")
            return render(request, 'login.html', {})
    else:
        return render(request, 'login.html', {})

def profile_view(request):
    return render(request, 'profile.html', {})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("login"))