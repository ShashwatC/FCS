from django.shortcuts import render
from django.shortcuts import redirect


# Create your views here.

def index(request):
    return render(request, 'home/index.html')


def login_success(request):
    if request.user.groups.filter(name="customer").exists():
        return redirect("customer")
    elif request.user.groups.filter(name="merchant").exists():
        return redirect("merchant")
    elif request.user.groups.filter(name="sysadmin").exists():
        return redirect("sysadmin")
    elif request.user.groups.filter(name="employee").exists():
        return redirect("employee")
    elif request.user.groups.filter(name="manager").exists():
        return redirect("manager")
    else:
        return redirect("/")
