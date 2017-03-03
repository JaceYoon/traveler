from django.shortcuts import render,redirect
from .models import User
from django.contrib import messages
# Create your views here.
def index(request):
    return redirect("home:main")

def main(request):
    return render(request, "LR/index.html")

def register(request):
    viewsResponse = User.objects.ValidForm(request.POST)
    if viewsResponse['isRegistered']:
        request.session['id'] = viewsResponse['user'].id
        request.session['name'] = viewsResponse['user'].name
        return redirect('travel:home')
    else:
        for error in viewsResponse['errors']:
            messages.error(request, error)
        return redirect('home:index')


def success(request):
    if 'id' not in request.session:
        messages.error(request, 'Must be logged in')
        return redirect('home:index')

def login(request):
    viewsResponse = User.objects.login_user(request.POST)
    if viewsResponse['isLoggedIn']:
        request.session['id'] = viewsResponse['user'].id
        request.session['name'] = viewsResponse['user'].name
        return redirect('travel:home')
    else:
        for error in viewsResponse['errors']:
            messages.error(request, error)
        return redirect('home:index')

def logout(request):
    request.session.clear()
    return redirect('home:index')
