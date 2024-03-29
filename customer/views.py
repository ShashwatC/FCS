from django.http import Http404
from django.shortcuts import render, redirect
from home.choices import R_MAP

import math, random
from bank.models import Account, Transaction, Deposit, Withdraw, Profile, Pending, OTPInfo
from home.pki import decrypt
from customer.forms import DepositForm, WithdrawForm, TransferForm, ProfileForm, HighTransferForm, OTPForm

from .forms import DetailsForm
from django.core.mail import send_mail


def generateOTP(len):
    digits = "0123456789"
    OTP = ""
    for i in range(len) : 
        OTP += digits[math.floor(random.random() * 10)] 
    return OTP


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
        if not acc['pending']:
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
    form = DepositForm({'account_number': str(acc.id)})
    return render(request, 'customer/deposit.html', {'acc': acc.id, 'form': form})


def deposit_comp(request):
    user = request.user
    if check(user):
        return check(user)
    form = DepositForm(request.POST)
    i1 = int(form['account_number'].data)
    acc1 = Account.objects.filter(owner=user).get(id=i1)
    bal = int(form['amount'].data)
    user1 = request.user

    if not form.is_valid():
        return render(request, 'customer/deposit.html', {'acc': acc1.id, 'form': form})

    print(bal)
    new_deposit = Deposit.objects.create(owner=user1, owner_acc=acc1, amount=bal, pending=True)
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
    user = request.user
    if check(user):
        return check(user)

    form = WithdrawForm(request.POST)
    i1 = int(form['account_number'].data)
    acc1 = Account.objects.filter(owner=user).get(id=i1)
    bal = int(form['amount'].data)
    user1 = request.user

    if not form.is_valid():
        return render(request, 'customer/withdraw.html', {'acc': acc1.id, 'form': form})

    if acc1.balance < bal:
        return render(request,"customer/transaction_failed.html")

    cond = 0
    if bal < 10000:
        new_withdraw = Withdraw.objects.create(owner=user1, owner_acc=acc1, amount=bal, pending=False)
        new_withdraw.save()
        acc1.balance -= bal
        acc1.save()
    else:
        new_withdraw = Withdraw.objects.create(owner=user1, owner_acc=acc1, amount=bal, pending=True)
        new_withdraw.save()
        cond = 1

    return render(request, 'customer/withdraw_comp.html', {'cond': cond})


def transfer(request):
    user = request.user
    if check(user):
        return check(user)

    form = request.POST
    acc = Account.objects.filter(owner=user).get(id=form['acc_num'])
    print(acc)
    form = TransferForm({'account_number': str(acc.id)})
    return render(request, 'customer/transfer.html', {'acc': acc.id, 'form': form})


def transfer2(request):
    user = request.user
    if check(user):
        return check(user)
    form = request.POST
    acc = form['id']
    print(acc)
    F = TransferForm({'account_to': str(acc)})
    return render(request, 'customer/merchanttransfer.html', {'form': F})


def transfer_comp(request):
    user = request.user
    if check(user):
        return check(user)

    form = TransferForm(request.POST)

    print(type(form['account_number']))
    i1 = int(form['account_number'].data)
    i2 = int(form['account_to'].data)
    acc1 = Account.objects.filter(owner=user).get(id=i1)
    acc2 = Account.objects.get(id=i2)
    bal = int(form['amount'].data)

    if not form.is_valid():
        return render(request, 'customer/transfer.html', {'acc': acc1.id, 'form': form})

    user1 = request.user
    user2 = acc2.owner

    cond = 0

    if(acc1.balance<bal):
    	return render(request,"customer/transaction_failed.html")

    if bal < 10000:
        new_transaction = Transaction.objects.create(sender=user1, sender_acc=acc1, receiver=user2, receiver_acc=acc2,
                                                     amount=bal, pending=False)
        new_transaction.save()
     
        acc1.balance -= bal
        acc2.balance += bal
        
        acc1.save()
        acc2.save()
    elif bal <= 100000:
    	new_transaction = Transaction.objects.create(sender=user1, sender_acc=acc1, receiver=user2, receiver_acc=acc2,
                                                     amount=bal, pending=True)
    	new_transaction.save()

    elif bal <= 10000000:
        OTP = generateOTP(6)
        message = "OTP: " + OTP
        send_mail('SBI: Transaction OTP', message, 'securebankingincorporated@gmail.com', [user1.email])
        new_transaction = Transaction.objects.create(sender=user1, sender_acc=acc1, receiver=user2, receiver_acc=acc2,
                                                     amount=bal, pending=True)
        new_transaction.save()
        cond = 1
        otp_rec = OTPInfo.objects.create(trans_id=new_transaction.id,otp=OTP)
        otp_rec.save()
        cond = 1
        Form = OTPForm()
        return render(request, 'customer/verify.html',{'trans_id':new_transaction.id,'form':Form})

    else:
        form_h = HighTransferForm({'account_number':form['account_number'].data ,
                                   'amount':form['amount'].data,
                                   'account_to': form['account_to'].data})
        return render(request, 'customer/pki.html', {'form': form_h})

    return render(request, 'customer/trans_pend.html', {'cond': cond})


def otp_verify(request):
    user = request.user
    if check(user):
        return check(user)
    form = request.POST
    ID = int(form['trans_id'])
    OTP = OTPForm(request.POST)
    Original = OTPInfo.objects.get(pk=ID)
    p=0
    if(OTP['otp'].data == Original.otp):
        p=1
        Original.approved=True
        Original.save()
    else:
        p=0
        Original.delete()
    print(p)
    return render(request, 'customer/otp_pend.html',{'cond':p})


def tranfer_pki(request):
    user = request.user
    if check(user):
        return check(user)

    form_h = HighTransferForm(request.POST)
    private_key = Profile.objects.get(user=request.user).private_key
    response = form_h['response'].data
    print(response,private_key)
    try:
        balance = decrypt(response,private_key)
    except:
        return render(request, 'customer/verification_failed.html')

    print(balance)
    if int(balance) == int(form_h['amount'].data):
        i1 = int(form_h['account_number'].data)
        i2 = int(form_h['account_to'].data)
        user1 = request.user
        acc1 = Account.objects.filter(owner=user1).get(id=i1)
        acc2 = Account.objects.get(id=i2)
        user2 = acc2.owner
        new_transaction = Transaction.objects.create(sender=user1, sender_acc=acc1, receiver=user2, receiver_acc=acc2,
                                                     amount=balance, pending=True)
        new_transaction.save()
        print(new_transaction)
        return render(request, 'customer/verification_success.html')
    else:
        return render(request, 'customer/verification_failed.html')


def edit_prof(request):
    user = request.user
    if check(user):
        return check(user)

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        user = request.user
        if form.is_valid():
            if Pending.objects.filter(user=user).count() == 0:
                new_pending = Pending.objects.create(user=user)
                new_pending.first_name = form['first_name'].data
                new_pending.last_name = form['last_name'].data
                new_pending.email_address = form['email_address'].data
                new_pending.mobile_number = form['mobile_number'].data
                new_pending.save()
                return render(request, 'customer/edit_prof_done.html')
    else:
        form = ProfileForm()
    return render(request, 'customer/create.html', {'form': form})


def create_acc(request):
    user = request.user
    if check(user):
        return check(user)

    if request.method == 'POST':
        form = DetailsForm(request.POST)

        if form.is_valid():
            init_balance = int(form.cleaned_data.get('initial_balance'))
            user = request.user
            new_account = Account.objects.create(balance=init_balance, owner=user)
            new_account.save()
            return render(request, 'customer/account_created.html')
    else:
        form = DetailsForm()
    return render(request, 'customer/create.html', {'form': form})
