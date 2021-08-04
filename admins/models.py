from django.db import models
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
