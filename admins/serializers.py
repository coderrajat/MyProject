from rest_framework import serializers
from . import models as admin_models
from accounts import models as account_models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
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
class admin_form(serializers.ModelSerializer):
    class Meta:
        model=account_models.Admins
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
        model=account_models.Admins()
        exclude=('token','otp')

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
