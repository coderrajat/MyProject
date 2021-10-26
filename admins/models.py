from os import name
from django.db import models
from accounts import models as accounts_models
class CMS(models.Model):
    name=models.CharField(max_length=200,unique=True)
    content = models.TextField(null=True,blank=True)
class faq(models.Model):
    question=models.TextField(null=True,blank=True)
    answer=models.TextField(null=True,blank=True)
class social_media_settings(models.Model):
    company_url=models.CharField(max_length=2000,blank=True,default='')
    facebook_url=models.CharField(max_length=2000,blank=True,default='')
    twitter_url=models.CharField(max_length=2000,blank=True,default='')
    instagram_url=models.CharField(max_length=2000,blank=True,default='')
    linkedin_url=models.CharField(max_length=2000,blank=True,default='')
    youtube_url=models.CharField(max_length=2000,blank=True,default='')
class image_settings(models.Model):
    deafult_profile_pic=models.ImageField(default='deafult_profile_pic.jpeg',help_text = "1:1")
    default_parking_spot_pic=models.ImageField(default='provider/images/default_parking_spot_pic.jpg',help_text = "2:1")
class general_settings(models.Model):
    company_name = models.CharField(max_length=30, null=True, default='Parking Bud')
    company_email = models.EmailField(verbose_name="email", max_length=60, null=True, default='parkingbud@gmail.com')
    company_country_code = models.CharField(max_length=10,default='')
    company_phone_no = models.CharField(max_length=20,null=True,blank=True)
    company_address_line_1=models.CharField(max_length=200,null=True,blank=True)
    company_address_line_2=models.CharField(max_length=200,null=True,blank=True)
    company_country=models.CharField(max_length=100,null=True,blank=True)
    company_city=models.CharField(max_length=100,null=True,blank=True)
    company_state=models.CharField(max_length=100,null=True,blank=True)
    company_zip_code=models.CharField(max_length=100,null=True,blank=True)
    timezone=models.CharField(max_length=30,null=True,blank=True)
class SMTP_setting(models.Model):
    twilio_phone_number=models.CharField(max_length=100,blank=True,default='')
    sendgrid_sender_email=models.EmailField()
class artist(models.Model):
    name=models.CharField(max_length=400)
    artist_origin=models.TextField()
    photo=models.ImageField(upload_to='images/artist',default='deafult_profile_pic.jpeg')
class album(models.Model):
    name=models.CharField(max_length=400)
    artist=models.ManyToManyField(artist,related_name='albums_artist')
    year=models.DateTimeField()
    cover=models.ImageField(upload_to='images/album',default='deafult_profile_pic.jpeg')
class songs(models.Model):
    name=models.CharField(max_length=400,blank=True,default='')
    song_mp3=models.FileField(upload_to='images/songs')
    cover=models.ImageField(upload_to='images/songs',default='deafult_profile_pic.jpeg')
    album=models.ForeignKey(album,on_delete=models.SET_NULL,null=True,related_name='album')
  
    artist=models.ManyToManyField(artist,related_name='artist')
    number_of_likes=models.IntegerField()
    likes=models.TextField()#the user id will be here who like the song eg: 1,2
    lyrics=models.CharField(max_length=4000,blank=True,default='')
    genres=models.CharField(max_length=400,blank=True,default='')
    charts=models.CharField(max_length=400,blank=True,default='')
    year=models.DateTimeField()

class playlist_admin(models.Model):
    name=models.CharField(max_length=400) 
    #title
    cover=models.ImageField(upload_to='images/playlist',default='deafult_profile_pic.jpeg')
    gener=models.CharField(max_length=400)
    songs=models.ManyToManyField(songs,related_name='admin_playlist')

class SubscriptionPlan(models.Model):

    plan_name=models.CharField(max_length=200)
    descriptions=models.CharField(max_length=500,default="",null=True)
    date_created=models.DateTimeField(null=True,blank=True)
    cost=models.CharField(max_length=100,default="",null=True,blank=True)
    status=models.CharField(max_length=100,default="",null=True)
    is_pause=models.BooleanField(default=False)

class Notification_admin(models.Model):
    title=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    message=models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)




    

  
    

   

