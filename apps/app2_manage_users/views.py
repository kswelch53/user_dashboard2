from django.shortcuts import render, HttpResponse, redirect
from apps.app1_login_register.models import User
from django.contrib import messages
import re, bcrypt

# displays user group on manage_users.html
# accessed by clicking Administrators link on home page
def index(request):
    print("This is the index method in app2 views.py")

# If not logged in, users will be returned to the home page
    if 'user_level' not in request.session:
        return redirect('loginreg:index')
# Only level 9 users can access manage_users.html
    elif request.session['user_level'] == 9:
        print("User is an administrator")

    # saving users group in context
        context = {
            'users': User.objects.all()
        }

        all_users=User.objects.all()
        print("All users are:", all_users)
        return render(request, 'app2_manage_users/manage_users.html', context)
# Logged-in users who are not a level 9 will be returned to the home page
    else:
        print("User is not an administrator. User level is:", request.session['user_level'])
        return redirect('loginreg:index')


# displays add_user.html; admins can add a new user
def add_user(request):
    print("This is the add_users method in app2 views.py")
    if request.method == 'POST':
        response_from_models = User.objects.validate_user(request.POST)
        print("Response from models:", response_from_models)
        return redirect('admins:index')
    return render(request, 'app2_manage_users/add_user.html')


# Administrators can edit individual users by clicking Edit link on manage_users.html
def edit_user(request, id):
    print("This is the edit_users method in app2 views.py")

# gets user object to be edited
    context = {
        'user': User.objects.get(id=id)
    }
    print("edit_user method, user is:", id)

# updates user object with data from form
    if request.method == 'POST':
        edit_user = User.objects.get(id=id)
        print("Editing user:", edit_user.first_name, edit_user.last_name)

        edit_user.email = request.POST['email']


        # needs check for duplicate email


        # saves form data in database:
        edit_user.first_name = request.POST['first_name']
        edit_user.last_name = request.POST['last_name']
        edit_user.level = request.POST['level']
        edit_user.save()

# returns all user objects, including the edited object, to the page for display
        context = {
            'users': User.objects.all()
        }
        return render(request, 'app2_manage_users/manage_users.html', context)
# displays page before editing
    return render(request, 'app2_manage_users/edit_user.html', context)


# Admins can update password
def edit_password(request, id):
    if request.method == 'POST':
        edit_user = User.objects.get(id=id)
        print("Editing user:", edit_user.first_name, edit_user.last_name)
        edit_user.password = request.POST['password']
        edit_user.pw_confirm = request.POST['pw_confirm']

# password = pwconfirm validation; aborts if passwords don't match
        if not edit_user.password == edit_user.pw_confirm:
            redirect('admins:index')
        else:
            #hashes the updated password with bcrypt
            edit_user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
            edit_user.save()

    # returns all user objects, including the edited object, to the page for display
            context = {
                'users': User.objects.all()
            }
            return render(request, 'app2_manage_users/manage_users.html', context)
    else:
        context = {
            'user': User.objects.get(id=id)
        }
        return render(request, 'app2_manage_users/edit_user.html', context)


# asks Administrators whether they want to delete a user object
def deletecheck(request, id):
    print("This is deletecheck function in views.py")
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'app2_manage_users/delete_user.html', context)


#deletes a user from the database
def remove_user(request, id):
    print("This is the remove_user method in app3 views.py")
    User.objects.get(id=id).delete()
    context = {
        'users': User.objects.all()
    }
    return render(request, 'app2_manage_users/manage_users.html', context)
