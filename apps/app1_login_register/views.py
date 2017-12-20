from django.shortcuts import render, HttpResponse, redirect
from .models import User
from django.contrib import messages

# Create your views here.
def index(request):
    print("This is the index method in app1 views.py")
    return render(request, 'app1_login_register/index.html')


def register(request):
    print("This is the register method in app1 views.py")
    if request.method == 'POST':
        print("This is the POST register method in app1 views.py")
        print("Request.POST:", request.POST)
        response_from_models = User.objects.validate_user(request.POST)
        print("Response from models:", response_from_models)
        if response_from_models['status']:#if true
            # passed the validations and created a new user

            # user data can now be saved in session, by id:
            request.session['user_id'] = response_from_models['user'].id
            request.session['user_first_name'] = response_from_models['user'].first_name
            request.session['user_level'] = response_from_models['user'].level
            print(request.session['user_id'], request.session['user_first_name'], request.session['user_level'])

            # return redirect('loginreg:success')
            # return redirect('admins:index')#goes to index method in app2
            return redirect('messages:all_users')#goes to all_users method in app3

        else:#validation not passed
            for error in response_from_models['errors']:
                messages.error(request, error)
            return redirect('loginreg:register')
    return render(request, 'app1_login_register/register.html')


#linked from anchor tag on index.html; takes user to login.html
def login(request):
    print("This is the login method in app1 views.py")
    if request.method == 'POST':
        print("This is the POST login method in app1 views.py")
        print("Request.POST:", request.POST)
        response_from_models = User.objects.login_user(request.POST)
        print("Response from models:", response_from_models)
        if response_from_models['status']:#if true (validations are met):

            #saves user data in session, sends user to success page:
            request.session['user_id'] = response_from_models['user'].id
            request.session['user_first_name'] = response_from_models['user'].first_name
            request.session['user_level'] = response_from_models['user'].level
            print("Session is:", request.session['user_id'], request.session['user_level'])

            # return redirect('loginreg:success')
            # return redirect('admins:index')
            return redirect('messages:all_users')
            # return redirect('messages:index')#goes to all_users method in app3


        else:#validation not passed
            # no for-loop here; only 1 message will appear at a time
            # errors: either invalid email or invalid email/pw combo
            messages.error(request, response_from_models['errors'])
            return redirect('loginreg:login')
    else:
        return render(request, 'app1_login_register/login.html')

def logout (request):
    print("This is the logout method in app1 views.py")
    if request.method == 'POST':
        request.session.clear()#deletes everything in session
    return redirect('loginreg:index')
