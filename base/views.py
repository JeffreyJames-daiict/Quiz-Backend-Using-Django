from django.shortcuts import render, HttpResponse
from django.contrib.auth.models import User
from account.models import Profile

def home(request):
    
    # user_object = User.objects.get(username=request.user)
    # user_profile = Profile.objects.get(user = user_object)

    # context = {"user_profile" : user_profile}
    return render(request, 'welcome.html')
# Create your views here.
