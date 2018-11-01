from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from home.choices import R_MAP
from bank.models import Account,Transaction,Deposit, Withdraw, Pending, Profile


def check(user):
    if user.groups.count() == 0:
        return redirect("/accounts/login")

    if user.groups.count() == 1:
        raise Http404()

    user_group = user.groups.values('name')
    c = 0
    for u in user_group:
        if int(u['name']) == int(R_MAP['Employee']):
            c = 1
        print(c)

    if not c:
        raise Http404()


def index(request):
    user = request.user
    if check(user):
        return check(user)
    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'employee/index.html', {'name': name})


def approval(request):
    if request.method == 'POST':
        form = request.POST
        acc1 = Account.objects.get(pk=int(form['sen_acc']))
        acc2 = Account.objects.get(pk=int(form['rec_acc']))
        amount = int(form['amount'])
        acc2.balance += amount
        acc1.balance -= amount
        acc1.save()
        acc2.save()
        Transaction.objects.filter(pk = int(form['pkk'])).delete()

    user = request.user
    if check(user):
        return check(user)
    reqs = Transaction.objects.all()
    reques = []
    for acc in reqs:
        if(acc.amount<100000):
            reques.append((acc.sender, acc.sender_acc.id, acc.receiver, acc.receiver_acc.id, acc.amount,acc.pk))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'employee/transactions.html', {'req': reques, 'name': name})


def removal(request):
    if request.method == 'POST':
        form = request.POST
        Transaction.objects.filter(pk = int(form['pkk'])).delete()    
    user = request.user
    if check(user):
        return check(user)
    reqs = Transaction.objects.all()
    reques = []
    for acc in reqs:
        if(acc.amount<100000):
            reques.append((acc.sender, acc.sender_acc.id, acc.receiver, acc.receiver_acc.id, acc.amount,acc.pk))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'employee/removal.html', {'req': reques, 'name': name})


def vew(request):
    user = request.user
    if check(user):
        return check(user)
    reqs = Transaction.objects.all()
    reques = []
    for acc in reqs:
        if(acc.amount<100000):
            reques.append((acc.sender, acc.sender_acc.id, acc.receiver, acc.receiver_acc.id, acc.amount,acc.pk))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'employee/view.html', {'req': reques, 'name': name})


def acc_pen(request):
    if request.method == 'POST':
        form = request.POST

        acc = Account.objects.get(pk=form['pk'])
        acc.pending = False
        acc.save()

    user = request.user
    if check(user):
        return check(user)
    reqs = Account.objects.all()
    reques = []
    for acc in reqs:
        if acc.pending:
            reques.append((acc.pk, acc.balance))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'employee/account_pending.html', {'req': reques, 'name': name})

def withdraw(request):

    if request.method == 'POST':
        form = request.POST
        acc1 = Account.objects.get(pk=int(form['own_acc']))
        amount = int(form['amount'])
        acc1.balance -= amount
        acc1.save()
        Withdraw.objects.filter(pk = int(form['pkk'])).delete()

    user = request.user
    if check(user):
        return check(user)
    reqs = Withdraw.objects.all()
    reques = []
    for acc in reqs:
        if(acc.amount<100000):
            reques.append((acc.owner, acc.owner_acc.id, acc.amount, acc.pk))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'employee/withdraw.html', {'req': reques, 'name': name})

def deposit(request):
    if request.method == 'POST':
        form = request.POST
        acc1 = Account.objects.get(pk=int(form['own_acc']))
        amount = int(form['amount'])
        acc1.balance += amount
        acc1.save()
        Deposit.objects.filter(pk = int(form['pkk'])).delete()

    user = request.user
    if check(user):
        return check(user)
    reqs = Deposit.objects.all()
    reques = []
    for acc in reqs:
        if(acc.amount<100000):
            reques.append((acc.owner, acc.owner_acc.id, acc.amount, acc.pk))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'employee/deposit.html', {'req': reques, 'name': name})


def modify(request):
    if request.method == 'POST':
        form = request.POST
        user = User.objects.get(username = form['user'])
        pending = Pending.objects.get(user = user)
        new_profile = Profile.objects.get(user = user)
        new_profile.mobile_number = pending.mobile_number
        user.first_name = pending.first_name
        user.last_name = pending.last_name
        user.email = pending.email_address
        Pending.objects.filter(user = user).delete()
        user.save()
        new_profile.save()

    user = request.user
    if check(user):
        return check(user)
    reqs = Pending.objects.all()
    reques = []
    for acc in reqs:
        reques.append((acc.user.username, acc.first_name, acc.last_name, acc.email_address, acc.mobile_number))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'employee/modify.html', {'req': reques, 'name': name})