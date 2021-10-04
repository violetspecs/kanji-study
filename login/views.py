from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.models import User
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse

def index(request):
    return render(request, 'login/index.html')

def loginuser(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('quiz:index'))
    else:
        return HttpResponseRedirect(reverse('login:index'))

def signup(request):
    return render(request, 'login/signup.html')

def signupuser(request):
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    firstname = request.POST['firstname']
    lastname = request.POST['lastname']
    user = User.objects.create_user(username, email, password, last_name=lastname, first_name=firstname)
    user = authenticate(username=username, password=password)
    if user is not None:
        return HttpResponseRedirect(reverse('quiz:index'))
    else:
        return HttpResponseRedirect(reverse('login:index'))

def logoutuser(request):
    logout(request)
    return HttpResponseRedirect(reverse('login:index'))