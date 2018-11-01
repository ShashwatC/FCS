from django.http import Http404
from django.shortcuts import render, redirect
from home.choices import R_MAP
from bank.models import Account,Transaction,Deposit,Withdraw

from customer.forms import DepositForm, WithdrawForm, TransferForm
from .forms import DetailsForm


def check(user):
    if user.groups.count() == 0:
        return redirect("/accounts/login")

    if user.groups.count() == 1:
        return redirect("/accounts/pending")

    user_group = user.groups.values('name')

    c = 0
    for u in user_group:
        if int(u['name']) == int(R_MAP['Customer']):
            c = 1
        print(c)

    if not c:
        raise Http404()


def index(request):
    user = request.user
    if check(user):
        return check(user)
    bank_acct = Account.objects.filter(owner=user).values()
    accounts = []
    for acc in bank_acct:
        if acc['pending']==False:
            accounts.append((acc['id'], acc['balance']))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'customer/index.html', {'acc': accounts, 'name': name})


def account(request):
    user = request.user
    if check(user):
        return check(user)
    name = request.user.first_name + " " + request.user.last_name
    form = request.POST
    acc = Account.objects.filter(owner=user).filter(pending=False).get(id=form['acc_num'])
    return render(request, 'customer/account.html', {'acc': [(acc.id, acc.balance)], 'name': name, 'acc_no': acc.id})


def deposit(request):
    user = request.user
    if check(user):
        return check(user)
    form = request.POST
    acc = Account.objects.filter(owner=user).get(id=form['acc_num'])
    print(acc)
    F = DepositForm({'account_number': str(acc.id)})
    return render(request, 'customer/deposit.html', {'acc': acc.id, 'form': F})

def deposit_comp(request):

    form = DepositForm(request.POST)
    i1 = int(form['account_number'].data)
    acc1 = Account.objects.get(id = i1)
    bal = int(form['amount'].data)
    user1 = request.user
    if(bal<0):
        print("not valid")    #asdfaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

    new_deposit = Deposit.objects.create(owner = user1, owner_acc = acc1, amount = bal)
    new_deposit.save()

    return render(request, 'customer/deposit_comp.html')


def withdraw(request):
    user = request.user
    if check(user):
        return check(user)
    form = request.POST
    acc = Account.objects.filter(owner=user).get(id=form['acc_num'])
    print(acc)
    form = WithdrawForm({'account_number': str(acc.id)})
    return render(request, 'customer/withdraw.html', {'acc': acc.id, 'form': form})

def withdraw_comp(request):

    form = WithdrawForm(request.POST)
    i1 = int(form['account_number'].data)
    acc1 = Account.objects.get(id = i1)
    bal = int(form['amount'].data)
    user1 = request.user
    if(bal>acc1.balance):
        print("not valid")    #asdfaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    
    cond = 0
    if(bal<10000):
        acc1 -= bal
        acc1.save()
    else:
        new_withdraw = Withdraw.objects.create(owner = user1, owner_acc = acc1, amount = bal)
        new_withdraw.save()
        cond = 1

    return render(request, 'customer/withdraw_comp.html',{'cond':cond})


def transfer(request):
    user = request.user
    if check(user):
        return check(user)
    form = request.POST
    acc = Account.objects.filter(owner=user).get(id=form['acc_num'])
    print(acc)
    F = TransferForm({'account_number': str(acc.id)})
    return render(request, 'customer/transfer.html', {'acc': acc.id, 'form': F})

def transfer_comp(request):
    form = TransferForm(request.POST)
    print("asdjflkajslfjdalkdjflasjdflk")
    print(type(form['account_number']))
    i1 = int(form['account_number'].data)
    i2 = int(form['account_to'].data)
    acc1 = Account.objects.get(id = i1)
    acc2 = Account.objects.get(id = i2)
    bal = int(form['amount'].data)
    user1 = request.user
    user2 = acc2.owner
    if(bal<0):
        print("not valid")    #asdfaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa

    cond = 0    
    if(bal<10000):
        acc1.balance -= bal
        acc2.balance += bal
        acc1.save()
        acc2.save()
    else:
        new_transaction = Transaction.objects.create(sender = user1, sender_acc = acc1, receiver = user2, receiver_acc = acc2, amount = bal)
        new_transaction.save()
        cond = 1

    return render(request, 'customer/trans_pend.html', {'cond': cond})


def edit_prof(request):
    return 0


def create_acc(request):
    if request.method == 'POST':
        form = DetailsForm(request.POST)
        if form.is_valid():
            init_balance = int(form.cleaned_data.get('initial_balance'))
            user = request.user
            if init_balance < 0:
                print("to do")
            new_account = Account.objects.create(balance=init_balance, owner=user)
            print("this account in being saved")
            new_account.save()
            return render(request, 'customer/account_created.html')
    else:
        form = DetailsForm()
    return render(request, 'customer/create.html', {'form': form})
