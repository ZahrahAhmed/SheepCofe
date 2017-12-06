from django.shortcuts import render, redirect
from .forms import UserSignup, UserLogin
from django.contrib.auth import authenticate, login, logout

def usersignup(request):
    form = UserSignup()
    context = {"form": form, }
    if request.method == 'POST':
        form = UserSignup(request.POST)
        if form.is_valid():
            user = form.save()
            username = user.username
            password = user.password

            user.set_password(password)
            user.save()

            auth_user = authenticate(username=username, password=password)
            login(request, auth_user)

            return redirect("/")
        return redirect("sheepcofe:signup")
    return render(request, 'signup.html', context)

def userlogin(request):
    form = UserLogin()
    context = {"form": form, }
    if request.method == 'POST':
        form = UserLogin(request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            auth_user = authenticate(username=username, password=password)
            if auth_user is not None:
                login(request, auth_user)
                return redirect('/')
            return redirect("sheepcofe:login")
        return redirect("sheepcofe:login")
    return render(request, 'login.html', context)

def userlogout(request):
    logout(request)
    return redirect("/")