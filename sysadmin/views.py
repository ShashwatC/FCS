from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from home.choices import MAP, R_MAP
from django.contrib.auth.models import Group
from bank.models import Account,Transaction, Withdraw, Deposit


def check(user):
    if user.groups.count() == 0:
        return redirect("/accounts/login")

    if user.groups.count() == 1:
        return redirect("/accounts/pending")

    user_group = user.groups.values('name')
    c = 0
    for u in user_group:
        if int(u['name']) == int(R_MAP['SysAdmin']):
            c = 1
        print(c)

    if not c:
        raise Http404()



def index(request):
    user = request.user
    if check(user):
        return check(user)
    return render(request, 'sysadmin/index.html')

def del_internal(request):
    user = request.user
    if check(user):
        return check(user)

    if request.method == 'POST':
        form = request.POST
        User.objects.filter(username = form['user']).delete()

    reqs = User.objects.all()
    acc = []
    for r in reqs:
        print(r.username)
        print(r.groups.count())
        if r.groups.count()==2 and r.username != user.username:
            group_stored = int(r.groups.values('name').first()['name'])
            acc.append(( r.username, MAP[group_stored] ))
    return render(request, 'sysadmin/removal.html', {'req': acc})


def pending(request):

    user = request.user
    if check(user):
        return check(user)
    
    if request.method == 'POST':
        form = request.POST
        user = User.objects.get(username=form['name'])
        # user count should be 1, or some attack is happening
        if user.groups.count() == 1:
            group_stored = int(user.groups.values('name').first()['name'])
            group_in_request = R_MAP[form['group']]
            # groups should be same, or some attack is happening
            print("First",group_in_request, group_stored)
            if group_stored == group_in_request:
                print("Second",group_in_request, group_stored)
                new_group, created = Group.objects.get_or_create(name=5)
                user.groups.add(new_group)
    users = User.objects.all()
    user_groups = []
    for user in users:
        # 0 groups - registration incomplete
        # 1 group - registration done, not approved
        # 2 groups - registration done and approved
        if user.groups.count() == 1:
            group = user.groups.values('name').first()
            user_groups.append((user.username, MAP[int(group['name'])]))
    return render(request, 'sysadmin/pending.html', {'user_groups': user_groups})

def view_trans(request):
    user = request.user
    if check(user):
        return check(user)

    all_trans = Transaction.objects.all()
    all_withdraw = Withdraw.objects.all()
    all_deposit = Deposit.objects.all()
    return render(request, 'sysadmin/view.html', { 'trans': all_trans, 'withdraw' : all_withdraw, 'depoit' : all_deposit})

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
    for acc in reqs:
        if acc.pending:
            reques.append((acc.pk, acc.balance))

    name = request.user.first_name + " " + request.user.last_name
    return render(request, 'sysadmin/account_pending.html', {'req': reques, 'name': name})