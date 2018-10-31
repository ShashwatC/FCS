from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from home.choices import R_MAP
from bank.models import Account
from .models import Trans


def check(user):
    if user.groups.count() == 0:
        return redirect("/accounts/login")

    if user.groups.count() == 1:
        raise Http404()

    user_group = int(user.groups.values('name').first()['name'])

    if user_group != R_MAP['Employee']:
        print(user_group)
        raise Http404()


def index(request):
    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'employee/index.html',{'name' : name})

def approval(request):
    
    if request.method == 'POST':
        form = request.POST
        
        user1 = User.objects.get(username=form['u_id'])
        user2 = User.objects.get(username=form['r_id'])
        acc1 = Account.objects.get(owner=user1)
        acc2 = Account.objects.get(owner=user2)
        acc2.balance += acc1.balance
        acc1.balance = 0
        acc1.save()
        acc2.save()
        Trans.objects.filter(trans_id = form['tr_id']).delete()
    
    user = request.user
    if check(user):
        return check(user)
    reqs = Trans.objects.filter(owner=user).values()
    reques = []
    for acc in reqs:
        print(acc)
        reques.append((acc['trans_id'],acc['u_id'],acc['r_id']))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'employee/transactions.html',{'req': reques,'name' : name})

def removal(request):
    if request.method == 'POST':
        form = request.POST
        Trans.objects.filter(trans_id = form['tr_id']).delete()
    
    user = request.user
    if check(user):
        return check(user)
    reqs = Trans.objects.filter(owner=user).values()
    reques = []
    for acc in reqs:
        reques.append((acc['trans_id'],acc['u_id'],acc['r_id']))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'employee/removal.html',{'req': reques,'name' : name})

def vew(request):
    
    user = request.user
    if check(user):
        return check(user)
    
    reqs = Trans.objects.filter(owner=user).values()
    reques = []
    for acc in reqs:
        reques.append((acc['trans_id'],acc['u_id'],acc['r_id']))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'employee/view.html',{'req': reques,'name' : name})

def modify(request):
    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'employee/index.html',{'name' : name})