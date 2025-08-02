from django.shortcuts import render

# Create your views here.
def login(request):
    context = {
        'title':'Home-Autharization',

    }
    return render(request,'',context)
def profile(request):
    context = {
        'title':'Home-profile',

    }
    return render(request,'',context)
def registration(request):
    context = {
        'title':'Home-Registration',

    }
    return render(request,'',context)
def logout(request):
    context = {
        'title':'Home-Logout',

    }
    return render(request,'',context)