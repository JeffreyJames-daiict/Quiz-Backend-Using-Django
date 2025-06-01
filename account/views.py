from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User,auth
from django.contrib.auth.decorators import login_required
# check if the user is login or not 
from .models import Profile


# Create your views here.
def register(request):

    if request.user.is_authenticated:
        return redirect('profile', request.user.username)

    if request.method == 'POST':
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']    

        if password == password2:
            print("Password Match")

            # check if email is not same 
            if User.objects.filter(email= email).exists():
                messages.info(request,"Email already taken. Try to Login")
                return redirect('register')            
            
            # check if username is not same
            elif User.objects.filter(username = username).exists():
                messages.info(request,"Username already taken")
                return redirect('register', username)
            
            
            else:
                #Create User
                user = User.objects.create_user(username=username,email=email,password=password)
                user.save()

                #log in the user and redirect to profile 
                user_login = auth.authenticate(username=username,password=password)
                auth.login(request,user_login)

                #create profile for new user
                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user = user_model,email_address = email)
                new_profile.save()

                return redirect('profile')
            
        else:
            messages.info(request,"Password not Matching")
            return redirect('register')


    context = {}
    return render(request,"register.html",context)

@login_required(login_url='login')
def profile(request,username):
    #Profile User
    user_object2 = User.objects.get(username = username)
    user_profile2 = Profile.objects.get(user = user_object2)


    #Request User
    #when other user is seeing another profile hence request.user    
    user_object = User.objects.get(username=request.user)
    user_profile = Profile.objects.get(user = user_object)


    context = {"user_profile" : user_profile, "user_profile2" : user_profile2}
    return render(request,'profile.html',context)

def login(request):
    if request.user.is_authenticated:
        return redirect('profile', request.user.username)
                        
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            return redirect('profile',username)
        else:
            messages.info(request, "Credentials Invalid !")
            return redirect('login')

    return render(request,'login.html')

@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')