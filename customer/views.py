from django.http import Http404
from django.shortcuts import render


# Create your views here.
def index(request):
    user = request.user
    if user.groups.count() == 1:
        raise Http404("Poll does not exist")

    group_stored = int(user.groups.values('name').first()['name'])
    return render(request, 'customer/index.html')
