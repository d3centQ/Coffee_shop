from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import auth,messages
from django.http import HttpResponseRedirect
from django.urls import reverse
from carts.models import Cart

from carts.models import Cart
from users.forms import UserLoginForm, UserRegistrationForm, ProfileForm


# Create your views here.
def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            session_key = request.session.session_key
            if user:
                auth.login(request,user)
                messages.success(request, f"{username},You have been logged in")
                if session_key:
                    Cart.objects.filter(session_key=session_key).update(user=user)
                redirect_page = request.POST.get('next',None)
                if redirect_page and redirect_page != reverse('user:logout'):
                    return HttpResponseRedirect(request.POST.get('next'))


                return HttpResponseRedirect(reverse('main:index'))
    else:
        form = UserLoginForm()

    context = {
        'title':'Home-Autharization',
        'form': form,
        'messages': messages,

    }
    return render(request,'users/login.html',context)
@login_required(login_url='user:login')
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(data=request.POST,instance=request.user,files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated successfully")

            return HttpResponseRedirect(reverse('user:profile'))
    else:
        form = ProfileForm(instance=request.user)
    context = {
        'title':'Home-profile',
        'form': form,
        'messages': messages,

    }
    return render(request,'users/profile.html',context)
def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            user = form.save()

            if not request.session.session_key:
                request.session.save()
            session_key = request.session.session_key

            auth.login(request, user)

            if session_key:
                Cart.objects.filter(session_key=session_key).update(user=user)

            messages.success(request, f"{user.username}, you have been registered and logged in")
            return redirect('main:index')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = UserRegistrationForm()

    return render(request, 'users/registration.html', {
        'title': 'Home - Registration',
        'form': form,
    })


def users_cart(request):
    return render(request, 'users/users_cart.html')
def users_cart(request):
    return render(request,'users/users_cart.html')



@login_required(login_url='user:login')
def logout(request):
    messages.success(request, f"{request.user.username},You have been logged out")
    auth.logout(request)
    return redirect(reverse('main:index'))
