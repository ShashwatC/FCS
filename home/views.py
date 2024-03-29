from django.contrib.auth import authenticate, login
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from home.forms import DetailsForm
from bank.models import Profile
from home.pki import get_pair

# Create your views here.


def index(request):
    if request.user.groups.filter(name="0").exists():
        return redirect("/customer")
    elif request.user.groups.filter(name="1").exists():
        return redirect("/merchant")
    elif request.user.groups.filter(name="2").exists():
        return redirect("/employee")
    elif request.user.groups.filter(name="3").exists():
        return redirect("/manager")
    elif request.user.groups.filter(name="4").exists():
        return redirect("/sysadmin")
    else:
        return redirect("/accounts/login")



def pending(request):
    return render(request, 'registration/pending.html')


def login_success(request):
    if request.user.groups.filter(name="0").exists():
        return redirect("/customer")
    elif request.user.groups.filter(name="1").exists():
        return redirect("/merchant")
    elif request.user.groups.filter(name="2").exists():
        return redirect("/employee")
    elif request.user.groups.filter(name="3").exists():
        return redirect("/manager")
    elif request.user.groups.filter(name="4").exists():
        return redirect("/sysadmin")
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
            mobile_number = form.cleaned_data.get('mobile_number')
            new_group, created = Group.objects.get_or_create(name=form.cleaned_data.get('choice'))
            user.groups.set([new_group])
            user.save()
            return redirect('/accounts/login_success/')
    else:
        user = request.user
        public_key_str = "This is the not the first time you're accessing the page, your public key was given" \
                         " to you the first time"
        if Profile.objects.filter(user=user).count() == 0:
            private_key_str, public_key_str = get_pair()
            profile = Profile(user=user, mobile_number="", private_key=private_key_str)
            profile.save()
        form = DetailsForm({'public_key':public_key_str})
    return render(request, 'registration/register_more.html',{'form': form})