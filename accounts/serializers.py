from rest_framework import serializers
from . import models
from django.core.exceptions import ValidationError
from rest_framework.exceptions import AuthenticationFailed
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
            print(i,ord(i))
            #pass
        else:
            print(i,ord(i),'error')
            return False
    return True
#print(is_allowed('is,allowed'))
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
    '''
    if not is_serise(val):
        raise ValidationError(
            _('password must not be a sequence (12345678 or abcdefgh) '),
            params={'val': val},
        )
    if not is_only_one_character(val):
        raise ValidationError(
            _('password must not be a sequence (12345678 or abcdefgh) '),
            params={'val': val},
        )'''
def is_all_number(val):
    for i in val:
        if ord(i)>57 or ord(i)<48:
            raise ValidationError(
                _('Phone Number should only contain numbers'),
                params={'val': val},
            )

#https://www.django-rest-framework.org/api-guide/validators/#function-based
class admin_data(serializers.ModelSerializer):
    class Meta:
        model=models.Admins
        exclude=('password','token','otp')
class userlogin(serializers.Serializer):
    email=serializers.CharField(max_length=200)
    password=serializers.CharField(max_length=155,required=False)
class send_otp_to_email(serializers.Serializer):
    email=serializers.EmailField()
class check_otp(serializers.Serializer):
    otp=serializers.IntegerField()
    email=serializers.EmailField()
class create_admin_password(serializers.Serializer):
    otp=serializers.IntegerField()
    email=serializers.CharField()
    password=serializers.CharField(validators=[validate])
    confirm_password=serializers.CharField()

class password(serializers.Serializer):
    password=serializers.CharField(required=False,validators=[validate])
    confirm_password=serializers.CharField(required=False)
class signup_user(serializers.ModelSerializer):
    referral_code=serializers.CharField(required=False)
    class Meta():
        model=models.Admins
        fields=('country_code',"phone_number","referral_code")
class admins_forms(serializers.ModelSerializer):
    class Meta():
        model=models.Admins
        exclude=('token',)
class check_user_otp(serializers.Serializer):
    otp=serializers.IntegerField()
    id=serializers.CharField()
class user_data(serializers.ModelSerializer):
    class Meta:
        model=models.Users
        exclude=('password','token','otp')
class create_password(serializers.Serializer):
    otp=serializers.IntegerField()
    id=serializers.CharField()
    password=serializers.CharField(validators=[validate])
    confirm_password=serializers.CharField()
class signin_user(serializers.ModelSerializer):
    password=serializers.CharField()
    class Meta():
        model=models.Admins
        fields=('country_code',"phone_number","password")

#sk users data
class user_data(serializers.ModelSerializer):
    class Meta():
        model=models.Users
        fields=('__all__')
