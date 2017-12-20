from django.shortcuts import render, HttpResponse, redirect
from apps.app1_login_register.models import User
from .models import *
from django.contrib import messages
import re, bcrypt
# from django.core.urlresolvers import reverse

# Create your views here.
# def index(request):
    # response = "Hello, I am your third request!"
    # print("This is views.py in app3")
    # return HttpResponse(response)


# accessed by clicking All Users link on home page (app1)
# gets all user objects from database, id of user in session
# renders to all_users.html to display all users, link to edit_profile for session user:
def all_users(request):
    print("This is the all_users method in app3 views.py")
    if 'user_id' not in request.session:
        return redirect('loginreg:index')
# saving users group in context
    else:
        context = {
            'users': User.objects.all(),
            'user_id': request.session['user_id']
        }
        return render(request, 'app3_messages/all_users.html', context)


# accessed by clicking edit-your-profile link on All Users page
# gets session user's object from database and renders page by id
# renders to edit_profile.html, displays form for editing user name/email
def edit_profile(request, id):
    print("This is the edit_profile method in app3 views.py")
    user = User.objects.get(id=request.session['user_id'])
    print("NOT POST")
    print("User is: #", user.id, user.first_name, user.last_name)
    context = {
        'user': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'app3_messages/edit_profile.html', context)


# route for form data in Edit Info box on edit_profile.html
# allows users to change their name and email
# accessed by Save button, edited data changed in database
def edit_info(request, id):
    print
    ("This is the edit_info method in app3 views.py")

# checking id
    print("User ID is:", id)

# when the form to edit user name and email is submitted:
    if request.method == "POST":
        print("POST")

# updates session user's object in database and returns to all_users page
        edit_user = User.objects.get(id=id)
        print("User is: #", edit_user.id, edit_user.email, edit_user.first_name, edit_user.last_name)
        edit_user.email = request.POST['email']
        edit_user.first_name = request.POST['first_name']
        edit_user.last_name = request.POST['last_name']
        edit_user.save()
        print("Edited user:", edit_user.email, edit_user.first_name, edit_user.last_name)

# needs check for duplicate email

# ALWAYS REDIRECT after a post request
# the updated user data will appear on the all_users page
        return redirect('messages:all_users')
# will redirect to the same page even if the data isn't updated
    else:
        return redirect('messages:all_users')


# route for form data in Change Password box on edit_profile.html
# allows users to change their password
# accessed by Update Password button, edited data changed in database
def change_pw(request, id):
    if request.method == 'POST':
        edit_user = User.objects.get(id=id)
        print("Editing user:", edit_user.first_name, edit_user.last_name)
        edit_user.password = request.POST['password']
        edit_user.pw_confirm = request.POST['pw_confirm']

# needs password = pwconfirm validation

        #hashes the updated password with bcrypt
        edit_user.password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        edit_user.save()

# ALWAYS REDIRECT after a post request
        return redirect('messages:all_users')
# will redirect to the same page even if the data isn't updated
    else:
        return redirect('messages:all_users')


# TO COME: route for form data in Edit Description box on edit_profile.html
def edit_desc(request, id):
    print("This is edit_desc method in app3 views.py")
    return redirect('messages:all_users')
    # return redirect('messages:user_posts')


# ***** POSTS NOT WORKING YET *****
# ***** Refer to The_Wall for posting functionality *****
# accessed by name-links on both All Users and Manage Users pages
# renders to profile.html, which displays users' profile data by id
# all users can access profile pages and add posts
def profile(request, id):
    print("This is the profile method in app3 views.py")

    # context = {
    # user_post object is all posts sent to a user (10)
        # 'posts_to_user': User_posts.objects.all(id=id)
    # }


# saving individual user in context to display at top of profile page
    context = {
    # User object is for user name clicked on
        'user': User.objects.get(id=id),
    # User_posts object is all posts sent to the above user
        # 'posts_to_user': User_posts.objects.all(id=user_posts.id)
    }

    print("Profile page, user id is:", id)
    return render(request, 'app3_messages/profile.html', context)


# route for users' posts
def user_posts(request, id):
    print("This is the user_posts method in app3 views.py")

# creates new post object
# returns all post objects for display on profile page
    if request.method == 'POST':
        print("POST", id)
        newpost = User_posts.objects.create(post=request.POST['message'])
        print("New post is:", newpost)
        return redirect('messages:profile')
    return redirect('messages:profile')
