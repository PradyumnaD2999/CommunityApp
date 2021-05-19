from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from django.db.models.signals import post_save
from django.conf import settings
from autoslug import AutoSlugField

# Create your models here.

class Profile1(models.Model):
    user1 = models.OneToOneField(User, on_delete=models.CASCADE)
    image1 = models.ImageField(default='default.png', upload_to='images/')
    slug1 = AutoSlugField(populate_from='user')
    bio1 = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    linkedIn = models.CharField(max_length=255, blank=True)
    contact = models.CharField(max_length=255, blank=True)
    graduation= models.DateField()
    email = models.EmailField(max_length = 254)
    name = models.CharField(max_length=255, blank=True)
    id_proof= models.IntegerField() 
    friends1 = models.ManyToManyField("self", blank=True)

    
    def __str__(self):
        return str(self.user1.username)

    def get_absolute_url(self):
        return "/users/{}".format(self.slug)

#class FriendRequest(models.Model):
 #   to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user', on_delete=models.CASCADE)
  #  from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user', on_delete=models.CASCADE)
   # timestamp = models.DateTimeField(auto_now_add=True)

    #def __str__(self):
       # return "From {}, to {}".format(self.from_user.username, self.to_user.username)