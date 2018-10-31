from django.http import Http404
from django.shortcuts import render, redirect
from home.choices import R_MAP
from bank.models import Account


def check(user):
    """
    Functionality:
        If user is not logged in, redirect him to log in page
        If user is trying to access a page he shouldn't access, don't let him
    Behaviour:
        Returns redirection if user not logged in
        Raises 404 error if logged in but wrong page
        Returns None if everything is okay
    How to user:
        if check(user):
            return check(user)
        # If execution is here then user is good to go, write your code now
    """
    if user.groups.count() == 0:
        return redirect("/accounts/login")

    if user.groups.count() == 1:
        raise Http404()

    user_group = int(user.groups.values('name').first()['name'])

    if user_group != R_MAP['Merchant']:
        raise Http404()

# Create your views here.
def index(request):
    user = request.user
    if check(user):
        return check(user)

    # Account.objects.filter is when multiple objects are returned
    # Account.objects.get is for when single object is returned
    bank_accs = Account.objects.filter(owner=user).values()
    accounts = []
    for acc in bank_accs:
        accounts.append((acc['id'],acc['balance']))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'merchant/index.html',{'acc': accounts, 'name': name})


def account(request):
    user = request.user
    if check(user):
        return check(user)
    name = request.user.first_name + " " + request.user.last_name
    form = request.POST
    acc = Account.objects.filter(owner=user).get(id=form['acc_num'])

    return render(request, 'merchant/account.html', {'acc': [(acc.id,acc.balance)], 'name': name})