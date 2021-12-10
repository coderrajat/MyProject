from django.db import models

# Create your models here.
class Admins(models.Model):
    email=models.EmailField(verbose_name="email", max_length=60, unique=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    password=models.TextField(default="")
    address_line_1=models.CharField(max_length=200,default='')
    address_line_2=models.CharField(max_length=200,default='')
    profile_pic=models.ImageField(upload_to='images/profile',default='deafult_profile_pic.jpeg')
    otp=models.CharField(max_length=200,default='')
    country_code=models.CharField(max_length=10)
    phone_number=models.CharField(max_length=15)
    country=models.CharField(max_length=100,default='')#(multiple=False)
    city=models.CharField(max_length=100,default='')
    state=models.CharField(max_length=100,default='')
    zip_code=models.CharField(max_length=100,default='')
    timezone=models.TextField(default="UTC")

    is_user_blocked=models.BooleanField(default=False)
    date_joined=models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login=models.DateTimeField(verbose_name='last login', auto_now=True)
    token=models.CharField(max_length=10,default='')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name']
class Users(models.Model):
    email=models.EmailField(verbose_name="email", max_length=60, unique=True)
    full_name=models.CharField(max_length=100)
    country_code=models.CharField(max_length=10)
    phone_number=models.CharField(max_length=15)
    password=models.TextField(default="")

    gender=models.CharField(max_length=15)#Male femail others
    facebook=models.CharField(max_length=2000,default="")
    instagram=models.CharField(max_length=2000,default="")
    bio=models.CharField(max_length=500,default="")
    profile_pic=models.ImageField(upload_to='images/profile',default='deafult_profile_pic.jpeg')
    otp=models.CharField(max_length=200,default='')


    is_user_blocked=models.BooleanField(default=False)
    is_varified=models.BooleanField(default=False)
    date_joined=models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login=models.DateTimeField(verbose_name='last login', auto_now=True)
    token=models.CharField(max_length=10,default='')
    subscription_plan=models.CharField(max_length=100,default='free')
    
    #USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["country_code","phone_number"]