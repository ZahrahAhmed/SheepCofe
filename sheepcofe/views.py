from django.shortcuts import render, redirect
from .forms import UserSignup, UserLogin, CoffeeForm
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal

def coffeeprice(x):
    total = x.bean.price + x.roast.price + (x.espresso_shots*Decimal(0.250))
    if x.steamed_milk:
        total+= Decimal(0.100)
    if x.powders.all().count()>0:
        for powder in x.powders.all():
            total+= powder.price
    if x.syrups.all().count()>0:
        for syrup in x.syrups.all():
            total+= syrup.price
    return total

def createcoffee(request):
    context = {}
    if not request.user.is_authenticated():
        return redirect("sheepcofe:login")
    form = CoffeeForm()
    if request.method == "POST":
        form = CoffeeForm(request.POST)
        if form.is_valid():
            coffee = form.save(commit=False)
            coffee.user = request.user
            coffee.save()
            form.save_m2m()
            coffee.price = coffeeprice(coffee)
            coffee.save()
            return redirect('/')
    context['form'] = form
    return render(request, 'createcoffee.html', context)

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