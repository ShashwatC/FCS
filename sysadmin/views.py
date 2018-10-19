from django.shortcuts import render
from django.contrib.auth.models import User
from home.choices import MAP, R_MAP
from django.contrib.auth.models import Group


def index(request):
    return render(request, 'sysadmin/index.html')


def pending(request):
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
