#from django.db.models import fields
#from django.db.models import fields
from rest_framework import serializers

from . import models as admin_models
from accounts import models as account_models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from accounts.models import Users

def is_small(data):
    for i in data:
        if ord(i)>=97 and ord(i)<=122:
            return True
    return False
def is_large(data):
    for i in data:
        if ord(i)>=65  and ord(i)<=90:
            return True
    return False
def is_num(data):
    for i in data:
        if ord(i)>=48  and ord(i)<=57:
            return True
    return False
def is_special(data):
    for i in ['!','@','#','$','%','^','&','*']:
        if i in data:
            return True
    return False
def is_serise(data):
    a=0
    len=len(data)
    for i in range(data):
        if i==len-1:
            pass
        else:
            if ord(data[i])-ord(data[1+i]) in (-1,1):
                pass
            else:
                return True
    return False
def is_only_one_character(data):
    a=0
    len=len(data)
    for i in range(data):
        if i==len-1:
            pass
        else:
            if data[i]==data[1+i]:
                pass
            else:
                return True
    return False
def is_allowed(data):
    for i in data:
        if (ord(i)>=97 and ord(i)<=122) or (ord(i)>=65  and ord(i)<=90) or (i in  ['!','@','#','$','%','^','&','*']) or (ord(i)>=48  and ord(i)<=57):
            continue

        else:

            return False
    return True

def validate(val):
    if len(val)<8:

        raise ValidationError(
            _('password must have at least 8 characters'),
            params={'val': val},
        )
    if not is_small(val):
        raise ValidationError(
            _('password must have at least 1 LowerCase Alphabet '),
            params={'val': val},
        )
    if not is_large(val):
        raise ValidationError(
            _('password must have at least 1 UpperCase Alphabet '),
            params={'val': val},
        )
    if not is_special(val):
        raise ValidationError(
            _('password must have at least 1 valid sepcial character  '),
            params={'val': val},
        )
    if not is_allowed(val):
        raise ValidationError(
            _('password must have only valid sepcial character  '),
            params={'val': val},
        )
    if not is_num(val):
        raise ValidationError(
            _('password must have at least 1 Numaric character'),
            params={'val': val},
        )

def is_all_number(val):
    for i in val:
        if ord(i)>57 or ord(i)<48:
            raise ValidationError(
                _('Phone Number should only contain numbers'),
                params={'val': val},
            )
def is_in_word_limit(val):
    if len(val.split(' '))>200:
        raise ValidationError(
            _('must me less then 200 words'),
            params={'val': val},
        )

# class admin_info(serializers.ModelSerializer):
#     class Meta:
#         model=account_models.User
#         fields=('first_name',
#         'last_name',
#         'email',
#         'profile_pic',
#         'country',
#         'city',
#         'zip_code',
#         'state',
#         'country_code',
#         'phone_number',
#         'address_line_1',
#         'address_line_2',
#         'timezone',
#         'last_login'
#         )
# class edit_admin_profile(serializers.ModelSerializer):
#     phone_number=serializers.CharField(required=False,validators=[is_all_number])
#     class Meta:
#         model=account_models.User
#         fields=('first_name',
#         'last_name',
#         'email',
#         'profile_pic',
#         'country',
#         'city',
#         'zip_code',
#         'state',
#         'country_code',
#         'phone_number',
#         'address_line_1',
#         'address_line_2',
#         'timezone'
#         )
# class view_admin_authorize(serializers.ModelSerializer):
#     class Meta:
#         model=admin_models.authorizations
#         fields=('__all__')
class admin_info(serializers.ModelSerializer):
    class Meta:
        model=account_models.Admins
        #validators=[validate]
        exclude=('id',
                'token',
                'otp',
                'is_user_blocked',
                'date_joined',
                'last_login',
                'password')

class admin_form(serializers.ModelSerializer):
    class Meta:
        model=account_models.Admins
        #validators=[validate]
        exclude=('id',
                'profile_pic',
                'token',
                'otp',
                'is_user_blocked',
                'date_joined',
                'last_login',
                'password')

class admin_data(serializers.ModelSerializer):
    class Meta:
        #model=account_models.Admins()
        model=account_models.Admins
        exclude=('token','otp','password','date_joined','last_login')




class password(serializers.Serializer):
    password=serializers.CharField(required=False,validators=[validate])
    confirm_password=serializers.CharField(required=False)
class change_password(serializers.Serializer):
    oldpassword=serializers.CharField(required=False,validators=[validate])
    password=serializers.CharField(required=False,validators=[validate])
    confirm_password=serializers.CharField(required=False)
class csm_about_us_api(serializers.ModelSerializer):
    class Meta:
        model=admin_models.CMS
        fields=('content',)

class faq_category(serializers.ModelSerializer):
    class Meta:
        model=admin_models.faq
        fields=('id','question','answer')
# class faq_category(serializers.ModelSerializer):
#     class Meta:
#         model=admin_models.faq_category
#         fields=('__all__')
# class faq_category_show(serializers.ModelSerializer):
#     count=serializers.CharField()
#     class Meta:
#         model=admin_models.faq_category
#         fields=('id','category_name','count')
#
# class faq(serializers.ModelSerializer):
#     class Meta:
#         model=admin_models.faq
#         fields=('__all__')
# class faq_create(serializers.ModelSerializer):
#     class Meta:
#         model=admin_models.faq
#         exclude=('id','category')
# class image_settings(serializers.ModelSerializer):
#     class Meta:
#         model=admin_models.image_settings
#         exclude=('id',)
# class image_settings_base64(serializers.ModelSerializer):
#     deafult_profile_pic=serializers.CharField()
#     default_parking_spot_pic=serializers.CharField()
# class smtp_settings_api(serializers.ModelSerializer):
#     class Meta:
#         model=admin_models.SMTP_setting
#         exclude=('id',)
#
# class social_media_settings(serializers.ModelSerializer):
#     class Meta:
#         model=admin_models.social_media_settings
#         exclude=('id',)
# class block_user(serializers.Serializer):
#     email=serializers.EmailField()

class faq(serializers.ModelSerializer):
    class Meta:
        model=admin_models.faq
        fields=('__all__')
class image_settings(serializers.ModelSerializer):
    class Meta:
        model=admin_models.image_settings
        exclude=('id',)
class image_settings_base64(serializers.ModelSerializer):
    deafult_profile_pic=serializers.CharField()
    default_parking_spot_pic=serializers.CharField()
class smtp_settings_api(serializers.ModelSerializer):
    class Meta:
        model=admin_models.SMTP_setting
        exclude=('id',)

class social_media_settings(serializers.ModelSerializer):
    class Meta:
        model=admin_models.social_media_settings
        exclude=('id',)
class general_settings_serializer(serializers.ModelSerializer):
    class Meta():
        model = admin_models.general_settings
        fields = ('__all__')
class pagination(serializers.Serializer):
    result_limit = serializers.IntegerField(max_value=5000, min_value=1, required=True)
    page=serializers.CharField(required=False)
    order_by=serializers.CharField(required=False)
    order_by_type=serializers.CharField(required=False)
class search_user(serializers.Serializer):
    search=serializers.CharField(required=False)
    subscription_plan=serializers.CharField(required=False)
class search_consumer_form(serializers.ModelSerializer):
    class Meta:
        model=account_models.Users
        #fields=('__all__')
        exclude=('password','token','otp','date_joined','last_login')


class artist_for_song_serializer(serializers.ModelSerializer):
    class Meta:
        model=admin_models.artist
        fields=('id', 'name')

class album_for_song_serializer(serializers.ModelSerializer):
    class Meta:
        model=admin_models.album
        fields=('id', 'name')

class song_data(serializers.ModelSerializer):
    artist = artist_for_song_serializer(many=True, read_only=True)
    album = album_for_song_serializer(read_only=True)

    class Meta:
        model=admin_models.songs
        fields=('id', 'cover', 'name', 'song_mp3', 'artist', 'album', 'genres','mixing','producer','writer','mastering','artwork','photographer')
        depth=1

class search(serializers.Serializer):
    search=serializers.CharField(required=False)

class search_song_in_artist(serializers.Serializer):
    search=serializers.CharField(required=False)
    genres=serializers.CharField(required=False)

class playlist_admin_data(serializers.ModelSerializer):
    class Meta:
        model=admin_models.playlist_admin
        fields=('id', 'name', 'cover', 'gener', 'songs')
        depth=1


class playlist_admin_form(serializers.ModelSerializer):
    # search=serializers.CharField(required=False)
    class Meta:
        model=admin_models.playlist_admin
        fields=('id','name','gener','songs','downloads','cover')
class Artist_Data(serializers.ModelSerializer):
    class Meta:
        model=admin_models.artist
        fields="__all__"
# to add a new artist
class Artist_Add_Data(serializers.ModelSerializer):
    class Meta:
        model=admin_models.artist
        fields=["id","name","artist_origin","photo","followers","songs"]

class Artist_data(serializers.ModelSerializer):
    class Meta:
        model=admin_models.artist
        fields=["id","name","artist_origin","photo","followers","songs"]

class Add_artist_serializer(serializers.ModelSerializer):
    class Meta:
        model=admin_models.artist
        fields=['name', 'artist_origin', 'photo']
        
# album section serializers
class all_album(serializers.ModelSerializer):
    class Meta:
        model = admin_models.album
        fields = ['id','name','year','cover', 'likes', 'downloads', 'songs']
        depth=1

class Add_album_serializer(serializers.ModelSerializer):
    class Meta:
        model = admin_models.album
        fields = ['name', 'year', 'cover']

class search_album(serializers.Serializer):
    search=serializers.CharField(required=False)

class songs_da_ta(serializers.ModelSerializer):
    class Meta:
        model=admin_models.songs
        
        exclude=('song_mp3',)
       

class albums_songs_search(serializers.Serializer):
    search=serializers.CharField(required=False)


class user_forms(serializers.ModelSerializer):
    class Meta:
        model=account_models.Users
        exclude=('password','token','date_joined','last_login','otp')
        #fields=('__all__')

class edit_user_forms(serializers.ModelSerializer):
    class Meta:
        model=account_models.Users
        exclude=('password','token','date_joined','last_login','otp', 'profile_pic')

class albums_Song_data(serializers.ModelSerializer):
    class Meta:
        model=admin_models.songs
        fields=["id","cover","name","song_mp3","album","artist"]
        depth=1

class SubscriptionPlan_data(serializers.ModelSerializer):
    class Meta:
        model=admin_models.SubscriptionPlan
        fields = ("__all__")
# to add a new subscription plan
class SubscriptionPlan_Data_Add(serializers.ModelSerializer):
    class Meta:
        model=admin_models.SubscriptionPlan
        fields = ("plan_name","descriptions","is_pause", "cost", "plan_type", "benefits")

class user_profile(serializers.ModelSerializer):
    class Meta:
        model=account_models.Users
        fields=('profile_pic',)
        #fields=('__all__')
class Notification_data(serializers.ModelSerializer):
    user_sender = user_profile(read_only=True)
    class Meta:
        model=admin_models.Notification_admin
        fields=["id", "created_at", "user_sender", "type_of_notification", "status"]
        depth=1


#to show only two fields[id&artist name in song information]
class Artist_Serializer_For_Song_Data(serializers.ModelSerializer):
    class Meta:
        model=admin_models.artist
        fields=["id","name"]

#to show only two fields[id&album name in song information]
class Album_Serializer_For_Song_Data(serializers.ModelSerializer):
    class Meta:
        model=admin_models.album
        fields=["id","name"]

class Song_data(serializers.ModelSerializer):
    album=Album_Serializer_For_Song_Data(read_only=True)
    artist=Artist_Serializer_For_Song_Data(many=True,read_only=True)
   
    class Meta:
        model=admin_models.songs
        fields=["id","name","song_mp3","album","artist","downloads","cover","year","genres","charts","lyrics","number_of_likes","likes",'mixing','producer','writer','mastering','artwork','photographer']
        depth=1

# to create a new song      
class Song_Add(serializers.ModelSerializer):
    class Meta:
        model=admin_models.songs
        fields=["id","name","artist","album","genres","charts","lyrics","admin_playlist"]
        
class Artist_Album_Data(serializers.ModelSerializer):
    class Meta:
        model=admin_models.album
        fields=["id","name","cover","songs"]
        depth=1

class Array_of_ids(serializers.Serializer):
    ids = serializers.CharField(required=False)

class Add_song_serializer(serializers.ModelSerializer):
    #artist = serializers.CharField(required=False)
    #admin_playlist = serializers.CharField(required=False)
    class Meta:
        model=admin_models.songs
        fields=('name', 'cover', 'album', 'year', 'genres', 'charts', 'lyrics','mixing','producer','writer','mastering','artwork','photographer' )


class Album_data(serializers.ModelSerializer):
    class Meta:
        model=admin_models.album
        fields=["id","name", "cover", 'songs', 'year']
        depth=2

class Artist_song_data(serializers.ModelSerializer):#for a particular artist
    class Meta:
        model=admin_models.songs
        fields=["id","name","song_mp3","album","genres","cover","artist"]
        depth=2

class Search_album_song(serializers.Serializer):
    search=serializers.CharField(required=False)

class Album_song_data(serializers.ModelSerializer):#for a particular artist
    class Meta:
        model=admin_models.songs
        fields=["id","name","song_mp3","genres","likes","downloads","album","artist"]
        depth=2
#to add song in album from database
class Song_album_data(serializers.ModelSerializer):
    class Meta:
        model=admin_models.songs
        exclude=["song_mp3"]

class User_Playlist_By_Admin(serializers.ModelSerializer):
    class Meta:
        model=admin_models.playlist_admin
        fields=["id","name","user"]


# to show only album_name(id) in user liked_song
class Album_Serializer_For_Liked_Songs(serializers.ModelSerializer):
    class Meta:
        model=admin_models.album
        fields=["id","name"]

# to show only artist_name(id) in user liked_song
class Artist_Serializer_For_Liked_Songs(serializers.ModelSerializer):
    class Meta:
        model=admin_models.artist
        fields=["id","name"]

#serializer for user liked_song in admin panel
class User_Liked_Songs_By_Admin(serializers.ModelSerializer):
    artist=Artist_Serializer_For_Liked_Songs(many=True,read_only=True)
    album=Album_Serializer_For_Liked_Songs(read_only=True)

    class Meta:
        model=admin_models.songs
        fields=["id","name","cover","album","artist"]


        
class User_Data_For_Subscription_Plan(serializers.ModelSerializer):
    class Meta:
        model=Users
        field=["id","full_name"]


class Admin_User_Subscription_Plan(serializers.ModelSerializer):
    #user=User_Data_For_Subscription_Plan(read_only=True)
    class Meta:
        model=admin_models.Subscription_History
        fields=["id","user","subscription","active","expire"]
        depth=1

class Genere_Serializer(serializers.ModelSerializer):
    class Meta: 
        model=admin_models.Generes
        fields=["id", "name",'cover']
        

class Charts_Serializer(serializers.ModelSerializer):
    class Meta:
        model=admin_models.charts_admin
        fields=("name", "gener")       

class Get_Charts_Serializer(serializers.ModelSerializer):
    class Meta:
        model=admin_models.charts_admin
        fields=("__all__")
        depth=1   
        
        
class Users_feedback(serializers.ModelSerializer):
    class Meta:
        model=admin_models.Feedback
        fields=["id","subject","message","user"]


class Add_recommended_song_serializer(serializers.Serializer):
    user_id = serializers.IntegerField(required=True)
    song_id = serializers.IntegerField(required=True)








