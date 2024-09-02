from readline import get_current_history_length
from tkinter import W
from django.shortcuts import render, redirect
import requests
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib import messages
from .models import AppUserManager, AppUser
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from dotenv import load_dotenv
import os
import re

def req_api42(request, token):
    headers = {'Authorization': f'Bearer {token}'}

	#  fetch api 42
    response = requests.get('https://api.intra.42.fr/v2/me', headers=headers)
    data = response.json()

	#  if 42 user in DB: redirect to user profile else add user to DB then send to user profile
    if response.status_code == 200:
        if AppUser.objects.filter(email=data['email']).exists():
            user = AppUser.objects.get(email=data['email'])
            if user.email == data['email']:
                return redirect('/app/')
        else:
            user = AppUser.objects.create_user(
					email = data['email'],
					password = data['email'],
					)
            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.username = data['email']
            user.school_id = data['id']
            user.save()
            return redirect('/app/')
    else:
        return render(request, 'pages/login.html', {'error': 'Impossible de récupérer les datas'})


@csrf_protect
def index(request):
    if request.method == 'POST' and request.session.get('authMethod', None) is None:
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        try:
            validate_password(password)
        except ValidationError as e:
            error_message = ', '.join(e.messages)
            return render(request, 'pages/index.html', {'error': error_message})
        try:
            validate_email(email)
        except ValidationError as e:
            return render(request, 'pages/index.html', {'error': 'Enter a valid email address.'})
        if password != confirm_password:
            return (render(request, 'pages/index.html', {'error': 'Differents passwords'}))
        if not re.match(r'^[a-zA-Z0-9]+$', username):
            return render(request, 'pages/index.html', {'error': 'Username must contain only alphanumeric characters.'})
        try:
            user = AppUser.objects.create_user(
                email=email,
                password=password,
			)
            user.first_name = first_name
            user.last_name = last_name
            user.username = username
            user.save()
            messages.success(request, 'User created successfully!')
            return redirect('/login')
        except Exception as e:
            return render(request, 'pages/index.html', {'error': 'Username already taken'})
    return render(request, "pages/index.html")

@csrf_protect
def login(request):
    load_dotenv()
    HOST_IP = os.environ.get('HOST_IP')
    SECRET_42 = os.environ.get('SECRET_42')

    user = get_user_model()
    if request.session.get('authMethod', None) is None:
        if request.method == 'POST'  :
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                request.session['authMethod'] = 'local'
                return redirect('/app/')
            else:
                return render(request, 'pages/login.html', {'error': 'Non valid credentials.'})
        elif request.method == 'GET' and not request.user.is_authenticated:
            code = request.GET.get("code")
            if not code:
                return render(request, 'pages/login.html', {'URL': f"https://{HOST_IP}:8443/login"})

            url_token = "https://api.intra.42.fr/oauth/token"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {
                "grant_type": "authorization_code",
                "client_id": "u-s4t2ud-e6514ae93c2f3f3c25c6c98db2627ae8b9c70362848bea099f4e972c73370ec3",
                "client_secret": {SECRET_42},
                "code": code,
                "redirect_uri": f"https://{HOST_IP}:8443/login"
            }

            response = requests.post(url_token, headers=headers, data=data)
            if response.status_code == 200:
                token = response.json().get("access_token")
                if token:
                    request.session['access_token'] = token
                    request.session['authMethod'] = 'school'
                    return req_api42(request, token)
                else:
                    return render(request, 'pages/login.html', {'error': 'Error while getting token'})
            else:
                return render(request, 'pages/login.html', {'error': 'Token exchange failed'})
        elif request.method == 'GET':
            return render(request, 'pages/login.html', {'URL': f"https://{HOST_IP}:8443/login"})
    else:
        return redirect('/app/')


def logout_normal(request):
    if 'authMethod' in request.session:
        request.session.pop('authMethod')
    request.session['authMethod'] = None
    auth_logout(request)
    messages.success(request, 'Logout successful!')
    return redirect('login')

def logout(request):
    if 'access_token' in request.session:
        if 'authMethod' in request.session:
            request.session.pop('authMethod')
        request.session['authMethod'] = None
        del request.session['access_token']
        messages.success(request, 'Logout successful!')
        return redirect('login')
    else:
        return(logout_normal(request))
    return render(request, 'pages/login.html', {'logout': 'Error while logout'})


def about(request):
    return render(request, "pages/about.html")


def howItWorks(request):
    return render(request, "pages/how-it-works.html")


def signup(request):
    return render(request, "pages/index.html")


# * user logged in
def loggedIn(request):
    return render(request, "pages/logged-in.html")


def pwdReset(request):
    return render(request, "pages/pwd-reset.html")


def dashboard(request):
    return render(request, "pages/dashboard.html")


def settings(request):
    return render(request, "pages/settings.html")


def app(request):
    return render(request, "app.html")
