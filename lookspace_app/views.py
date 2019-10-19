from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return render(request, 'lookspace_app/html/index.html')

def user_signup(request):
    return render(request, 'lookspace_app/html/user_signup.html')

def user_signin(request):
    return render(request, 'lookspace_app/html/user_signin.html')

def partner_signup(request):
    return render(request, 'lookspace_app/html/partner_signup.html')

def partner_signin(request):
    return render(request, 'lookspace_app/html/partner_signin.html')



