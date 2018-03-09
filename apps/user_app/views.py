from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.urlresolvers import reverse
from .models import User
from ..message_app.models import Message

# Create your views here.
def index(request):
    if 'user' not in request.session:
        return render(request, 'user_app/index.html')
    else:
        return redirect(reverse('message_app:index'))

def register(request):
    valid, res = User.objects.validateregister(request.POST)
    if valid:
        email = request.POST['email']
        getbyemail = User.objects.get(email=email)
        request.session['user'] = {
            'id': getbyemail.id,
            'username': getbyemail.username,
            'first_name': getbyemail.first_name,
            'last_name': getbyemail.last_name,
            'email': getbyemail.email
        }
        return redirect(reverse('message_app:index'))
    else:
        for error in res:
            messages.error(request, error)
        return redirect(reverse('user_app:index'))

def login(request):
    valid, res = User.objects.validatelogin(request.POST)
    if valid:
        email = request.POST['email']
        getbyemail = User.objects.get(email=email)
        request.session['user'] = {
            'id': getbyemail.id,
            'username': getbyemail.username,
            'first_name': getbyemail.first_name,
            'last_name': getbyemail.last_name,
            'email': getbyemail.email,
        }
        return redirect(reverse('message_app:index'))
    else:
        for error in res:
            messages.error(request, error)
        return redirect(reverse('user_app:index'))

def user(request, id):
    user = User.objects.get(id=id)
    context = {
        'user' : user,
        'messages' : Message.objects.filter(user = User.objects.get(id=id)),
    }
    return render(request, "user_app/user.html", context)

def logout(request):
    del request.session['user']
    return redirect(reverse('user_app:index'))
