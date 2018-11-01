from django.http import Http404
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from home.choices import R_MAP
from bank.models import Account,Transaction,Deposit, Withdraw


def check(user):
    if user.groups.count() == 0:
        return redirect("/accounts/login")

    if user.groups.count() == 1:
        return redirect("/accounts/pending")

    user_group = user.groups.values('name')
    c = 0
    for u in user_group:
        if int(u['name']) == int(R_MAP['Manager']):
            c = 1
        print(c)

    if not c:
        raise Http404()


def index(request):
    user = request.user
    if check(user):
        return check(user)
    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'manager/index.html', {'name': name})


def approval(request):
    user = request.user
    if check(user):
        return check(user)

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


    reqs = Transaction.objects.all()
    reques = []
    for acc in reqs:
        reques.append((acc.sender, acc.sender_acc.id, acc.receiver, acc.receiver_acc.id, acc.amount,acc.pk))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'manager/transactions.html', {'req': reques, 'name': name})


def removal(request):
    user = request.user
    if check(user):
        return check(user)

    if request.method == 'POST':
        form = request.POST
        Transaction.objects.filter(pk = int(form['pkk'])).delete()    

    reqs = Transaction.objects.all()
    reques = []
    for acc in reqs:
        reques.append((acc.sender, acc.sender_acc.id, acc.receiver, acc.receiver_acc.id, acc.amount,acc.pk))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'manager/removal.html', {'req': reques, 'name': name})


def vew(request):
    user = request.user
    if check(user):
        return check(user)

    reqs = Transaction.objects.all()
    reques = []
    for acc in reqs:
        reques.append((acc.sender, acc.sender_acc.id, acc.receiver, acc.receiver_acc.id, acc.amount,acc.pk))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'manager/view.html', {'req': reques, 'name': name})


def modify(request):
    user = request.user
    if check(user):
        return check(user)

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'manager/index.html', {'name': name})


def acc_pen(request):
    user = request.user
    if check(user):
        return check(user)

    if request.method == 'POST':
        form = request.POST

        acc = Account.objects.get(pk=form['pk'])
        acc.pending = False
        acc.save()

    reqs = Account.objects.all()
    reques = []
    print(reqs)
    for acc in reqs:
        if acc.pending:
            print(acc.pk, acc.balance)
            reques.append((acc.pk, acc.balance))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'manager/account_pending.html', {'req': reques, 'name': name})

def withdraw(request):
    user = request.user
    if check(user):
        return check(user)

    if request.method == 'POST':
        form = request.POST
        acc1 = Account.objects.get(pk=int(form['own_acc']))
        amount = int(form['amount'])
        acc1.balance -= amount
        acc1.save()
        Withdraw.objects.filter(pk = int(form['pkk'])).delete()

    reqs = Withdraw.objects.all()
    reques = []
    for acc in reqs:
        reques.append((acc.owner, acc.owner_acc.id, acc.amount, acc.pk))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'manager/withdraw.html', {'req': reques, 'name': name})

def deposit(request):
    user = request.user
    if check(user):
        return check(user)

    if request.method == 'POST':
        form = request.POST
        acc1 = Account.objects.get(pk=int(form['own_acc']))
        amount = int(form['amount'])
        acc1.balance += amount
        acc1.save()
        Deposit.objects.filter(pk = int(form['pkk'])).delete()

    reqs = Deposit.objects.all()
    reques = []
    for acc in reqs:
        reques.append((acc.owner, acc.owner_acc.id, acc.amount, acc.pk))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'manager/deposit.html', {'req': reques, 'name': name})
