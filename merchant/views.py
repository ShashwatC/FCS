import random

from django.http import Http404
from django.shortcuts import render, redirect
from home.choices import R_MAP
from bank.models import Account,Transaction,Deposit,Withdraw,Profile, Pending, OTPInfo

from home.pki import decrypt
from merchant.forms import DepositForm, WithdrawForm, TransferForm, ProfileForm
from customer.forms import HighTransferForm, OTPForm
import math

from django.core.mail import send_mail

from .forms import DetailsForm


def generateOTP(len):
    digits = "0123456789"
    OTP = ""
    for i in range(len) :
        OTP += digits[math.floor(random.random() * 10)]
    return OTP


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
        return redirect("/accounts/pending")
    user_group = user.groups.values('name')
    c = 0
    for u in user_group:
        if int(u['name']) == int(R_MAP['Merchant']):
            c = 1
        print(c)

    if not c:
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


def deposit(request):
    user = request.user
    if check(user):
        return check(user)

    form = request.POST
    acc = Account.objects.filter(owner=user).get(id=form['acc_num'])
    print(acc)
    F = DepositForm({'account_number': str(acc.id)})
    return render(request, 'merchant/deposit.html', {'acc': acc.id, 'form': F})


def deposit_comp(request):
    user = request.user
    if check(user):
        return check(user)

    form = DepositForm(request.POST)
    i1 = int(form['account_number'].data)
    acc1 = Account.objects.get(id = i1)
    bal = int(form['amount'].data)
    user1 = request.user
    new_deposit = Deposit.objects.create(owner = user1, owner_acc = acc1, amount = bal)
    new_deposit.save()

    return render(request, 'merchant/deposit_comp.html')


def withdraw(request):
    user = request.user
    if check(user):
        return check(user)

    form = request.POST
    acc = Account.objects.filter(owner=user).get(id=form['acc_num'])
    print(acc)
    form = WithdrawForm({'account_number': str(acc.id)})
    return render(request, 'merchant/withdraw.html', {'acc': acc.id, 'form': form})


def withdraw_comp(request):
    user = request.user
    if check(user):
        return check(user)

    form = WithdrawForm(request.POST)
    i1 = int(form['account_number'].data)
    acc1 = Account.objects.get(id = i1)
    bal = int(form['amount'].data)
    user1 = request.user
    if(bal>acc1.balance):
        return render(request,"merchant/transaction_failed.html")

    
    cond = 0
    if(bal<10000):
        acc1 -= bal
        acc1.save()
    else:
        new_withdraw = Withdraw.objects.create(owner = user1, owner_acc = acc1, amount = bal)
        new_withdraw.save()
        cond = 1

    return render(request, 'merchant/withdraw_comp.html',{'cond':cond})


def transfer(request):
    user = request.user
    if check(user):
        return check(user)

    form = request.POST
    acc = Account.objects.filter(owner=user).get(id=form['acc_num'])
    print(acc)
    F = TransferForm({'account_number': str(acc.id)})
    return render(request, 'merchant/transfer.html', {'acc': acc.id, 'form': F})


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
        return render(request, 'merchant/verification_failed.html')

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
        return render(request, 'merchant/verification_success.html')
    else:
        return render(request, 'merchant/verification_failed.html')



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
        return render(request, 'merchant/transfer.html', {'acc': acc1.id, 'form': form})

    user1 = request.user
    user2 = acc2.owner
    if(bal>acc1.balance):
        return render(request,"merchant/transaction_failed.html")
        
    cond = 0    
    if(bal<10000):
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
        otp_rec = OTPInfo.objects.create(trans_id=new_transaction.id, otp=OTP)
        otp_rec.save()
        cond = 1
        Form = OTPForm()
        return render(request, 'merchant/verify.html', {'trans_id': new_transaction.id, 'form': Form})

    else:
        form_h = HighTransferForm({'account_number': form['account_number'].data,
                                   'amount': form['amount'].data,
                                   'account_to': form['account_to'].data})
        return render(request, 'merchant/pki.html', {'form': form_h})

    return render(request, 'merchant/trans_pend.html', {'cond': cond})

def edit_prof(request):
    user = request.user
    if check(user):
        return check(user)


    if request.method == 'POST':
        form = ProfileForm(request.POST)
        user = request.user
        if form.is_valid():
            if(Pending.objects.filter(user = user).count()==0):
                new_pending = Pending.objects.create(user = user)
                new_pending.first_name = form['first_name'].data
                new_pending.last_name = form['last_name'].data
                new_pending.email_address = form['email_address'].data
                new_pending.mobile_number = form['mobile_number'].data
                new_pending.save()
                return render(request, 'merchant/edit_prof_done.html')
    else:
        form = ProfileForm()
    return render(request, 'merchant/create.html', {'form': form})


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
            print("this account in being saved")
            new_account.save()
            return render(request, 'merchant/account_created.html')
    else:
        form = DetailsForm()
    return render(request, 'merchant/create.html', {'form': form})

def pay_merch(request,id):
    user = request.user
    if check(user):
        return check(user)

    try:
        merchant = Account.objects.get(pk=id)
    except Account.DoesNotExist:
        raise Http404("Merchant not found")
    print(id)
    return render(request,'merchant/pay.html',{'id':id})