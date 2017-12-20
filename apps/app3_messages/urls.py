#app-level url code:
from django.conf.urls import url, include
from . import views

# app3_messages
urlpatterns = [
# route for rendering all_users.html:
    url(r'^$', views.all_users, name='all_users'),

# route for rendering edit_profile.html:
    url(r'^edit_profile/(?P<id>\d+)$', views.edit_profile, name='edit_profile'),

# route for sending form data in edit info box on edit_profile.html:
    url(r'^edit_info/(?P<id>\d+)$', views.edit_info, name='edit_info'),

# route for sending form data in change password box on edit_profile.html:
    url(r'^change_pw/(?P<id>\d+)$', views.change_pw, name='change_pw'),

# route for sending form data in edit description box on edit_profile.html:
    url(r'^edit_desc/(?P<id>\d+)$', views.edit_desc, name='edit_desc'),


    url(r'^profile/(?P<id>\d+)$', views.profile, name='profile'),


    url(r'^user_posts/(?P<id>\d+)$', views.user_posts, name='user_posts'),

    # url(r'^user_update$', views.user_update, name='user_update'),
    # url(r'^display_messages/(?P<id>\d+)$', views.display_messages, name='display'),
]
