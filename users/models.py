from django.db import models
from accounts.models import Users
from admins.models import songs

# Create your models here.


class Recommended_Songs_by_admin(models.Model):
    user=models.ForeignKey(Users,on_delete=models.SET_NULL,related_name='recommended_songs',null=True,blank=True)    
    songs=models.ManyToManyField(songs,blank=True,null=True, related_name='recommended_to_user')