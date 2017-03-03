from django.shortcuts import render,redirect
from ..LR.models import User
from .models import Travel
from django.contrib import messages
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
    if 'id' not in request.session:
        messages.error(request, 'Must be logged in')
        return redirect('home:index')
    context = {
        "travels" : Travel.objects.filter(travel_join__id=request.session['id']).order_by('start_date'),
        "othertravels" : Travel.objects.exclude(travel_join__id=request.session['id']).exclude(creator=request.session['id']).order_by('start_date'),
    }
    return render(request,"travel/main.html",context)

def logout(request):
    request.session.clear()
    return redirect('home:index')

def add(request):
    if 'id' not in request.session:
        messages.error(request, 'Must be logged in')
        return redirect('home:index')
    else:
        return render(request,"travel/add.html")

def create(request):
    viewsResponse = Travel.objects.add_plan(request.POST, request.session['id'])
    if viewsResponse['isRegistered']:
        return redirect(reverse('travel:home'))
    else:
        for error in viewsResponse['errors']:
            messages.error(request, error)
            return redirect('travel:add')

def info(request, id):
    context = {
        "travel_info" : Travel.objects.filter(id=id),
    }
    return render(request, "travel/info.html", context)

def join(request, id):
    travel_id = Travel.objects.get(id=id)
    Travel.objects.join_travel(travel_id, request.session["id"])
    return redirect('travel:home')
