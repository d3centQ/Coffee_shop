from django.shortcuts import render

# Create your views here.
def login(request):
    context = {
        'title':'Home-Autharization',

    }
    return render(request,'users/login.html',context)
def profile(request):
    context = {
        'title':'Home-profile',

    }
    return render(request,'users/profile.html',context)
def registration(request):
    context = {
        'title':'Home-Registration',

    }
    return render(request,'users/registration.html',context)
def logout(request):
    context = {
        'title':'Home-Logout',

    }
    return render(request,'',context)