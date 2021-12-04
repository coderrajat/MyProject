from django.db import models
from datetime import datetime
from accounts.models import Users  
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
    likes=models.CharField(max_length=400,null=True,blank=True)
    followers=models.CharField(max_length=400,null=True,blank=True)

    photo=models.ImageField(upload_to='images/artist',default='deafult_profile_pic.jpeg')
    most_played=models.IntegerField(default=0)
class album(models.Model):
    name=models.CharField(max_length=400)
    #artist=models.ManyToManyField(artist,related_name='albums_artist')
    year=models.DateField(default=datetime.now(), blank=True)
    cover=models.ImageField(upload_to='images/album',default='deafult_profile_pic.jpeg')
    likes=models.CharField(max_length=400,null=True,blank=True)
    downloads=models.CharField(max_length=400,null=True,blank=True)
    
gener_choices=(  #gener choices
        ('Pop','Pop'),
        ('Electronics','Electronics'),
        ('Classic','Classic'),
        ('Rock','Rock'),
        ('Acoustic','Acoustic'),
        ('Heavy Metal','Heavy Metal'),
        ('EDM','EDM'),
        ('Latin','Latin'),
        ('Spanish','Spanish'),
        ('Karaoke','Karaoke'),
        ('Funk','Funk'),
        ('Folk','Folk'),
        ('Reggae','Reggae'),
        ('Rap','Rap'),
        ('Trance','Trance'),
)

    
class songs(models.Model):
    name=models.CharField(max_length=400)
    song_mp3=models.FileField(upload_to='images/songs')
    cover=models.ImageField(upload_to='images/songs',default='deafult_profile_pic.jpeg')
    album=models.ForeignKey(album,on_delete=models.SET_NULL,null=True,related_name='songs')
    artist=models.ManyToManyField(artist, blank=True, related_name='songs')
    downloads=models.CharField(max_length=400,null=True,blank=True)
    number_of_likes=models.IntegerField(default=0)
    likes=models.ManyToManyField(Users,related_name="liked_song")#the user id will be here who like the song eg: 1,2
    lyrics=models.CharField(max_length=4000,blank=True,default='')
    genres = models.CharField(max_length=400, blank=True, default='POP', choices=gener_choices)
    charts=models.CharField(max_length=400,blank=True,default='')
    year=models.DateField(default=datetime.now(), blank=True)

class playlist_admin(models.Model):
    name=models.CharField(max_length=400) 
    #title
    cover=models.ImageField(upload_to='images/playlist',default='deafult_profile_pic.jpeg')
    gener=models.CharField(max_length=400,default='POP', choices=gener_choices)
    songs=models.ManyToManyField(songs,blank=True,null=True, related_name='admin_playlist')
    downloads=models.IntegerField( default=0)
    user=models.ForeignKey(Users,on_delete=models.SET_NULL,related_name='admin_playlist',null=True,blank=True)
    year=models.DateTimeField(auto_now_add=True)
   
  
Plan_Type=(
           ("Monthlyplan","Monthlyplan"),
           ("Weeklyplan","Weeklyplan"),
           ("Yearlyplan","Yearlyplan"),

)
class SubscriptionPlan(models.Model):

    plan_name=models.CharField(max_length=200)
    benefits=models.CharField(max_length=2000,null=True,blank=True)
    plan_type=models.CharField(max_length=50,null=True,blank=True,choices=Plan_Type)
    descriptions=models.CharField(max_length=500,default="",null=True)
    date_created=models.DateTimeField(null=True,blank=True,auto_now_add=True)
    cost=models.CharField(max_length=100,default="",null=True,blank=True)
    status=models.CharField(max_length=100,default="",null=True)
    is_pause=models.BooleanField(default=False)
   

#get notification
class Notification_admin(models.Model):
    title=models.CharField(max_length=100)
    type=models.CharField(max_length=100)
    message=models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True,null=True, blank=True)


#to show subscription history to user
class Subscription_History(models.Model):
    user=models.ForeignKey(Users,on_delete=models.CASCADE,null=True,blank=True,related_name="user")
    subscription=models.ForeignKey(SubscriptionPlan,on_delete=models.CASCADE,null=True,blank=True,related_name="subscription_plan")
    active=models.DateTimeField(default=datetime.now())
    expire=models.DateTimeField(default=datetime.now())
 


    



