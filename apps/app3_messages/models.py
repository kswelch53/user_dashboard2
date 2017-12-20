from django.db import models
from apps.app1_login_register.models import User

# Create your models here.
class User_profile(models.Model):
    user_id=models.OneToOneField(User)
    description=models.CharField(max_length=255)

class User_posts(models.Model):
    post = models.CharField(max_length=255)
    user_posts= models.ManyToManyField(User, related_name = "posts")
    created_at = models.DateTimeField(auto_now_add=True)

    
