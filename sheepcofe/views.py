from django.shortcuts import render, redirect
from .forms import UserSignup, UserLogin, CoffeeForm
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal
from django.http import JsonResponse
from .models import Bean, Roast, Syrup, Powder
import json

def price(request):
    totalprice = Decimal(0)

    bean_id = request.GET.get('bean')
    if bean_id:
        totalprice += Bean.objects.get(id=bean_id).price

    roast_id = request.GET.get('roast')
    if roast_id:
        totalprice += Roast.objects.get(id=roast_id).price

    syrups = json.loads(request.GET.get('syrups'))
    if len(syrups)>0:
        for syrup_id in syrups:
            totalprice += Syrup.objects.get(id=syrup_id).price

    powders = json.loads(request.GET.get('powders'))
    if len(powders)>0:
        for powder_id in powders:
            totalprice += Powder.objects.get(id=powder_id).price

    milk = request.GET.get('milk')
    if milk=='true':
        totalprice += Decimal(0.100)

    shots=request.GET.get('espresso_shots')
    if shots:
        totalprice += (int(shots)*Decimal(0.250))

    return JsonResponse(round(totalprice,3), safe=False)

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
	if not request.user.is_authenticated:
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