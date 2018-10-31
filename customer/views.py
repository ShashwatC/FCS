from django.http import Http404
from django.shortcuts import render, redirect
from home.choices import R_MAP
from bank.models import Account
from .forms import DetailsForm


def check(user):

    if user.groups.count() == 0:
        return redirect("/accounts/login")

    if user.groups.count() == 1:
        raise Http404()

    user_group = user.groups.values('name')

    c = 0
    for u in user_group:
        if int(u['name']) == int(R_MAP['Customer']):
            c = 1
        print(c)
        
    if(not c):
        raise Http404()

def index(request):
    user = request.user
    if check(user):
        return check(user)
    bank_accs = Account.objects.filter(owner=user).values()
    accounts = []
    for acc in bank_accs:
        if(acc['pending']==False):
            accounts.append((acc['id'],acc['balance']))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'customer/index.html',{'acc': accounts, 'name': name})


def account(request):
    user = request.user
    if check(user):
        return check(user)
    name = request.user.first_name + " " + request.user.last_name
    form = request.POST
    acc = Account.objects.filter(owner=user).get(id=form['acc_num'])

    return render(request, 'customer/account.html', {'acc': [(acc.id,acc.balance)], 'name': name})

def edit_prof(request):
    return 0

def create_acc(request):
    if request.method == 'POST':
        form = DetailsForm(request.POST)
        if form.is_valid():
            init_balance = int(form.cleaned_data.get('initial_balance'))
            user = request.user
            if(init_balance<0):
                print("to do")
            new_account = Account.objects.create(balance = init_balance, owner = user)
            print("this account in being saved")
            new_account.save()
            return render(request,'customer/account_created.html')
    else:
        form = DetailsForm()
    return render(request, 'customer/create.html',{'form':form})
