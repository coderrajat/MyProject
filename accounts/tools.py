
import random
import base64
import pytz,datetime

import secrets
import math
import bcrypt
from . import models
from admins import models as admin_models
from twilio.rest import Client
from django.conf import settings
from django.core.files.base import ContentFile
import json
def code(data):
    def code_(num):
        key=[
        ['x', 'K', '7', 'A', 'Z', '-'],
        ['U', 'd', 'B', 'w', 'i', 'C'],
        ['y', 'J', 'V', 'e', 'o', '1'],
        ['m', '_', 'f', '.', 'F', '2'],
        ['Y', 'D', 'E', 'r', 'T', '~'],
        ['t', 'O', 'z', 's', 'b', '5'],
        ['j', 'h', 'H', 'L', 'P', '3'],
        ['G', 'p', 'u', '8', 'N', 'I'],
        ['R', '0', 'l', '6', 'v', 'q'],
        ['W', 'Q', 'M', 'k', 'n', 'g']]
        ln=10
        s=[]
        while True:
            if num<=1:
                s.append(key[num][random.randint(0,5)])
                break
            t1=num//ln
            a=num%ln
            s.append(key[a][random.randint(0,5)])
            num=t1
        e=''
        for i in s[::-1]:
           e+=i
        return e
    spacer=['a', 'X', '4', 'S', 'c', '9']
    s=''
    for i in str(data):
        s+=code_(ord(i))+spacer[random.randint(0,5)]
    print(s)
    return s


def decode(data):
    key={'x': 0, 'K': 0, '7': 0, 'A': 0, 'Z': 0, '-': 0, 'U': 1, 'd': 1, 'B': 1, 'w': 1, 'i': 1, 'C': 1, 'y': 2, 'J': 2, 'V': 2, 'e': 2, 'o': 2, '1': 2, 'm': 3, '_': 3, 'f': 3, '.': 3, 'F': 3, '2': 3, 'Y': 4, 'D': 4, 'E': 4, 'r': 4, 'T': 4, '~': 4, 't': 5, 'O': 5, 'z': 5, 's': 5, 'b': 5, '5': 5, 'j': 6, 'h': 6, 'H': 6, 'L': 6, 'P': 6, '3': 6, 'G': 7, 'p': 7, 'u': 7, '8': 7, 'N': 7, 'I': 7, 'R': 8, '0': 8, 'l': 8, '6': 8, 'v': 8, 'q': 8, 'W': 9, 'Q': 9, 'M': 9, 'k': 9, 'n': 9, 'g': 9}
    spacer=['a', 'X', '4', 'S', 'c', '9']
    ln=10
    for i in spacer:
        data=data.replace(i,'#')
    data=data[:len(data)-1].split('#')
    op=''
    for i in data:
        l=0
        g=0
        for k in list(i)[::-1]:
           l+=key[k]*(ln**g)
           g+=1
        op+=chr(l)
    print(op)
    return(op)

def codetoken(id,type='User',time=365*99,token=''):
    return code(type+'='+code(str(id))+','+
        str(datetime.datetime.now(tz=pytz.UTC)+datetime.timedelta(days=time))+','+token)

def decodetoken(data):

    r= decode(data).split(',')
    print(r)
    r[0]=r[0].split('=')
    r[0][1]=decode(r[0][1])
    return [*r[0],r[1],r[2]]

def get_user(usertype,id,time,token):
    if usertype=='admin':
        user=list(models.Admins.objects.filter(id=id))
        if user!=[]:
            user=user[0]
            if user.token==token:
                return user
            else:
                return []
        else:

            return []
    elif usertype=='users':
        user=list(models.Users.objects.filter(id=id))
        if user!=[]:
            user=user[0]
            if user.token==token:
                return user
            else:
                return []
        else:
            return []
    else:
        return []


# def email_changes(requestPOST,user_tem,subject='',header='',footer='',mail_to=''):
#     s=header
#     for ii in requestPOST:
#
#         if  (requestPOST[ii]!=str(user_tem[ii])):
#
#             if (requestPOST[ii]==str(user_tem[ii]).lower()):
#                 continue
#             if (str(type(user_tem[ii]))=="<class 'bool'>" and (requestPOST[ii]!=str(user_tem[ii]).lower())):
#                 s+=beautify_variable(ii)+': Previous='+str(user_tem[ii])+' Changed='+str(requestPOST[ii])+'\n'
#                 continue
#             s+=beautify_variable(ii)+': Previous='+str(user_tem[ii])+' Changed='+str(requestPOST[ii])+'\n'
#     s+=footer
#
#     try:
#         send_mail(subject,
#                     str(s),
#                     list(admin_models.SMTP_setting.objects.filter(id=1))[0].sendgrid_sender_email,
#                     [mail_to])
#     except Exception as e:
#         pass
def beautify_variable(s):
    return s.replace('_',' ').capitalize()
def beautify_errors(*args):
    s=''
    for i in args:
        for k in i:
            s+=beautify_variable(k)+' : '+i[k][0]+'\n'
    return s
def send_sms(to,data):
    account_sid = settings.ACCOUNT_SID
    auth_token = settings.AUTH_TOKEN
    #account_sid='ACd9f25f76012a61b20630ca4c4d39b440'
    #auth_token='d0b8cb13d6bd7cf67bc1a2ea2b55193f'
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                         body=data,#"Join Earth's mightiest heroes. Like Kevin Bacon.",
                         #from_=list(admin_models.SMTP_setting.objects.filter(id=1))[0].twilio_phone_number,
                         #to=to#'+15558675310'
                         #body='Hi',
                         from_='+12069008228',
                         to='+919958365127'
                     )
    print("this works?")
    print(message.sid,message)
    return message.sid

def get_base64_to_img(image_data):
    formats, imgstr = image_data.split(';base64,')
    ext = formats.split('/')[-1]
    data = ContentFile(base64.b64decode(imgstr))
    return( data,ext)

def convert_str_to_json_array(str):
   # x= []
   # for i in str.split(','):
    #  x.append(json.dumps(int(i)))
    
    #return json.loads(json.dumps(x))
    #print("helllo",x)
    #return x

    return json.loads(json.dumps(str.split(',')))

def send_admin_notification(title,type,message):
    notification=admin_models.Notification_admin.objects.create(title=title,type=type,message=message)
    notification.save()
    

        