from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.usersignup),
	path('login/', views.userlogin),
	path('logout/', views.userlogout),
]

