from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from home.forms import DetailsForm

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
        return redirect("/accounts/more")


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            uname = form.cleaned_data.get('username')
            pword = form.cleaned_data.get('password1')
            user = authenticate(username=uname, password=pword)
            login(request,user)
            return redirect('/accounts/more')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def registration_details(request):
    if request.method == 'POST':
        form = DetailsForm(request.POST)
        if form.is_valid():
            user = request.user
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.email = form.cleaned_data.get('email_address')
            new_group, created = Group.objects.get_or_create(name=form.cleaned_data.get('choice'))
            user.groups.set([new_group])
            return redirect('/')
    else:
        form = DetailsForm()
        print(form)
        return render(request, 'registration/register_more.html',{'form' : form})