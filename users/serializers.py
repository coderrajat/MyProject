from rest_framework import serializers
from admins import models as admin_models
from accounts import models as account_models
from users import models as user_model
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

class password(serializers.Serializer):
    password=serializers.CharField(required=False,validators=[validate])
    confirm_password=serializers.CharField(required=False)
class change_password(serializers.Serializer):
    oldpassword=serializers.CharField(required=False,validators=[validate])
    password=serializers.CharField(required=False,validators=[validate])
    confirm_password=serializers.CharField(required=False)

class pagination(serializers.Serializer):
    result_limit = serializers.IntegerField(max_value=20, min_value=1, required=True)
    page=serializers.CharField(required=False)
    order_by=serializers.CharField(required=False)
    order_by_type=serializers.CharField(required=False)
class song_data(serializers.ModelSerializer):
    # playlist_admin=
    class Meta:
        model=admin_models.songs
        fields=('__all__')
        depth=2
class search_song(serializers.Serializer):
    search=serializers.CharField(required=False)
class playlist_admin_data(serializers.ModelSerializer):
    # search=serializers.CharField(required=False)
    class Meta:
        model=admin_models.playlist_admin
        fields=('__all__')
        depth=2
class playlist_admin_form(serializers.ModelSerializer):
    # search=serializers.CharField(required=False)
    class Meta:
        model=admin_models.playlist_admin
        fields=('name','gener')