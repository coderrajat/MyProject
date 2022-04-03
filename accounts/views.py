from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.db.models import Q
import bcrypt
from . import tools
import datetime
import secrets
import random
#
from admins import models as admin_models
from accounts import models as accounts_models
from . import serializers
from users import models as user_models

def login_not_required(*ag,**kg):
    def inner(func):
        def wrapper(*args,**kwargs):
            print('-----------------------------------------',args[1].META)
            if 'HTTP_AUTHORIZATION'not in args[1].META :
                return func(*args,**kwargs)
            else:
                print('-=-=-=-',args[1].META['HTTP_AUTHORIZATION'])
                if args[1].META['HTTP_AUTHORIZATION']=='':
                    return func(*args,**kwargs)
                else:
                    return Response({'success':'false','error_msg':'USER IS LOGGEDIN','errors':{},'response':{}},status=status.HTTP_200_OK)
                return Response({'success':'false','error_msg':'USER IS LOGGEDIN','errors':{},'response':{}},status=status.HTTP_200_OK) #HTTP_401_UNAUTHORIZED

        return wrapper
    return inner
def login_required(*ag,**kg):
    def inner(func):
        def wrapper(*args,**kwargs):
            # print(args[1].META['HTTP_AUTHORIZATION'])
            if 'HTTP_AUTHORIZATION'in args[1].META :
                print(args[1])
                try:
                    data=tools.decodetoken(args[1].META['HTTP_AUTHORIZATION'])
                    print(data)
                    time=datetime.datetime.strptime(data[2].split('.')[0],'%Y-%m-%d %H:%M:%S')
                except:
                    return Response({'success':'false','error_msg':'invalid token','errors':{},'response':{}},status=status.HTTP_200_OK) 
                if len(data)==4 and time>datetime.datetime.now():
                    uzr= tools.get_user(*data)
                    if uzr!=[]:
                        print('#########',uzr.token)
                        if uzr.token=='':
                            return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_200_OK)
                        return func(*args,**kwargs)
                    else:
                        return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_200_OK)
                return Response({'success':'false','error_msg':'token expire','errors':{},'response':{}},status=status.HTTP_200_OK)
            else:
                return Response({'success':'false','error_msg':'no HTTP_AUTHORIZATION ','errors':{},'response':{}},status=status.HTTP_200_OK)
            return func(*args,**kwargs)
        return wrapper
    return inner
def login_admin(userid,token=''):
    token=tools.codetoken(userid,type='admin',token=token)
    return token
def login_user(userid,token=''):
    token=tools.codetoken(userid,type='users',token=token)
    return token
def logout_admin(token):
    try:
        data=tools.decodetoken(token)
        uzr=list(accounts_models.Admins.objects.filter(id=data[1]))

        if uzr!=[]:
            uzr=uzr[0]
            uzr.token=''
            uzr.save()
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
def logout_user(token):
    try:
        data=tools.decodetoken(token)
        uzr=list(accounts_models.Users.objects.filter(id=data[1]))

        if uzr!=[]:
            uzr=uzr[0]
            uzr.token=''
            uzr.save()
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False

class login_admin_api(APIView):
    @login_not_required()
    def get(self,request):
        f1=serializers.userlogin()
        return Response(f1.data,status=status.HTTP_200_OK)
    @login_not_required()
    def post(self,request):
        f1=serializers.userlogin(data=request.data)
        if (f1.is_valid()):
            user=list(accounts_models.Admins.objects.filter(email=request.POST['email'].lower()))
            if user!=[]:
                user=user[0]
            else:
                return Response({'success':'false',
                                    'error_msg':'User does not exist',
                                    'errors':'Invalid email',
                                    'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

            password=str(request.POST['password']).encode('utf-8')
            hash_pass=user.password.encode('utf-8')
            #print(password,hash_pass)
            if bcrypt.checkpw(password,hash_pass):
                sec=''
                for i in range(10):
                    sec+=secrets.choice(secrets.choice([chr(ii) for ii in range(45,123)]))

                user.token=sec
                user.last_login=datetime.datetime.now()
                user.save()
                re=login_admin(user.id,token=sec)
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{'user':[serializers.admins_forms(user).data],},
                                    'token':re,
                                },status=status.HTTP_200_OK)
            return Response({'success':'false',
                                'error_msg':'user_not_authenticated',
                                'response':{},
                                'errors':dict(f1.errors),
                                },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success':'false',
                                'error_msg':'log_in_parameters_not_correct',
                                'errors':dict(f1.errors),
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
                             
class logout_api(APIView):
    @login_required()
    def get(self,request):
        val=logout_admin(request.META['HTTP_AUTHORIZATION'])
        if val:
            return Response({'success':'true',
            'error_msg':'',
            'response':{},

            },status=status.HTTP_200_OK)
        else:
            print(val)
            return Response({'success':'false',
                                'error_msg':'Logout fail',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

class logout_user_api(APIView):
    @login_required()
    def get(self,request):
        val=logout_user(request.META['HTTP_AUTHORIZATION'])
        if val:
            return Response({'success':'true',
            'error_msg':'',
            'response':{},

            },status=status.HTTP_200_OK)
        else:
            print(val)
            return Response({'success':'false',
                                'error_msg':'Logout fail',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
class get_email(APIView):
    def get(self,request):
        # f0=serializers.password()
        f1=serializers.send_otp_to_email()

        return Response({**f1.data,
                            },status=status.HTTP_200_OK)
    def post(self,request):
        f1=serializers.send_otp_to_email(data=request.POST)
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':tools.beautify_errors({**dict(f1.errors)}),
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        uzr=list(accounts_models.Admins.objects.filter(email=request.POST['email']))
        if uzr==[]:
            return Response({'success':'false',
                                'error_msg':'User does not exist',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        uzr=uzr[0]
        uzr.otp=random.randint(1000,9999)
        uzr.save()
        try:
            send_mail("Resetting your Mayani Admin password",
                        """you otp for resetting the password is """+str(uzr.otp),
                        list(admin_models.SMTP_setting.objects.filter(id=1))[0].sendgrid_sender_email,
                        [request.POST['email']])
        except Exception as e:
             return Response({'success':'false',
                                 'error_msg':'please try again later'+str(list(admin_models.SMTP_setting.objects.filter(id=1))[0].sendgrid_sender_email),
                                 'errors':'',
                                 'response':str(e),
                                 },status=status.HTTP_400_BAD_REQUEST)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':serializers.admin_data(uzr).data,
                            },status=status.HTTP_200_OK)
                            
class check_admin_otp(APIView):
    def get(self,request):
        # f0=serializers.password()
        f1=serializers.check_otp()

        return Response({**f1.data,
                            },status=status.HTTP_200_OK)
    def post(self,request):
        f1=serializers.check_otp(data=request.POST)
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':tools.beautify_errors({**dict(f1.errors)}),
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        uzr=list(accounts_models.Admins.objects.filter(email=request.POST['email']))
        if uzr==[]:
            return Response({'success':'false',
                                'error_msg':'invalid email',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        uzr=uzr[0]
        if uzr.otp==request.POST["otp"]:
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':serializers.admin_data(uzr).data,
                                },status=status.HTTP_200_OK)
        else:
            return Response({'success':'false',
                                'error_msg':'invalid OTP',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
class change_password_admin(APIView):
    def get(self,request):
        # f0=serializers.password()
        f1=serializers.create_admin_password()
        return Response({**f1.data,
                            },status=status.HTTP_200_OK)
    def post(self,request):
        f1=serializers.create_admin_password(data=request.POST)
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':tools.beautify_errors({**dict(f1.errors)}),
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        if request.POST["password"]!=request.POST["confirm_password"]:
            return Response({'success':'false',
                                'error_msg':'password and confirm_password dose not match',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        uzr=list(accounts_models.Admins.objects.filter(email=request.POST['email']))
        if uzr==[]:
            return Response({'success':'false',
                                'error_msg':'invalid email',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        uzr=uzr[0]
        if uzr.otp!=request.POST["otp"]:
            return Response({'success':'false',
                                'error_msg':'invalid OTP',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        password=request.POST['password'].encode('utf-8')
        uzr.password=bcrypt.hashpw(password,bcrypt.gensalt())
        print('----',uzr.password)
        uzr.password=uzr.password.decode("utf-8")
        print(uzr.password)
        uzr.is_varified=True
        uzr.save()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':serializers.admin_data(uzr).data,
                            },status=status.HTTP_200_OK)
# class admin_forget_password(APIView):
#     def
class signup_user(APIView):
    def get(self,request):
      
        f1=serializers.signup_user()

        return Response({**f1.data,"confirm_password":'',
                            },status=status.HTTP_200_OK)
    def post(self,request):
        f1=serializers.signup_user(data=request.POST)
        if not ( f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':tools.beautify_errors({**dict(f1.errors)}),
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_200_OK)
        uzr=list(accounts_models.Users.objects.filter(Q(country_code=request.POST['country_code'])&Q(phone_number=request.POST['phone_number'])))
        if uzr!=[]:
            uzr=uzr[0]
            if uzr.is_varified==True:
                return Response({'success':'false',
                                    'error_msg':'User already exist',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_200_OK)
            else:
              uzr.delete()
        uzr=accounts_models.Users()
        history=admin_models.Points_History()
        
        notify_user=user_models.Notification_user()
        if request.POST['referral_code']!='':
            val=int(request.POST['referral_code'],16)
            try:
                result=accounts_models.Users.objects.get(id=val)
            except:
                 return Response({'success':'false',
                                    'error_msg':'referral code is not valid',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_200_OK)
            if result.subscription_plan.lower()=='weekly':
                result.invitation_points+=30
                result.referral_count+=1
                result.save()
                uzr.signup_points=25
                uzr.save()
                var1=25
                history.user=result
                history.receive_track='Invite a friend +30 Points'
                history.receive_track_name=str(result.referral_count)+' invite'
                history.save()
                notify_user.user=result
                notify_user.type_of_notification='You recieved +30 Invitation points'
                notify_user.save()
                
            elif result.subscription_plan.lower()=='monthly':
                result.invitation_points+=125
                result.referral_count+=1
                result.save()
                uzr.signup_points=50
                var1=50
                history.user=result
                history.receive_track='Invite a friend +125 Points'
                history.receive_track_name=str(result.referral_count)+' invite'
                history.save()
                notify_user.user=result
                notify_user.type_of_notification='You recieved +125 Invitation points'
                notify_user.save()
            elif result.subscription_plan.lower()=='yearly':
                result.invitation_points+=1500
                result.referral_count+=1
                result.save()
                uzr.signup_points=125
                uzr.save()
                var1=125
                history.user=result
                history.receive_track='Invite a friend +1500 Points'
                history.receive_track_name=str(result.referral_count)+' invite'
                history.save()
                notify_user.user=result
                notify_user.type_of_notification='You recieved +1500 Invitation points'
                notify_user.save()
            else:
                result.invitation_points+=10
                result.referral_count+=1
                result.save()
                uzr.signup_points=7
                uzr.save()
                var1=7
                history.user=result
                history.receive_track='Invite a friend +10 Points'
                history.receive_track_name=str(result.referral_count)+' invite'
                history.save()
                notify_user.user=result
                notify_user.type_of_notification='You recieved +10 Invitation points'
                notify_user.save()
        else:
            uzr.signup_points=5
            uzr.save()
            var1=5

        uzr.country_code=request.POST["country_code"]
        uzr.phone_number=request.POST["phone_number"]
        if request.POST['password']==request.POST['confirm_password']:
            password=request.POST['password'].encode('utf-8')
            password=bcrypt.hashpw(password,bcrypt.gensalt())
            uzr.password=password.decode("utf-8")
        else:
            return Response({'success':'false',
                                    'error_msg':'Confirm Password does not match',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
        uzr.otp=random.randint(1000,9999)
        uzr.save()
        uzr.referral_code=hex(uzr.id)
        uzr.save()
        obj=accounts_models.Users.objects.get(id=uzr.id)
        notify_user.user=obj
        notify_user.type_of_notification='You recieved +'+str(var1)+' SignUp points'
        notify_user.save()
        notify=admin_models.Notification_admin()
        notify.user_sender=obj
        notify.type_of_notification=str(uzr.phone_number)+' join Mayani music family'
        notify.save()
        plan=admin_models.SubscriptionPlan.objects.filter(plan_type='Free')
        sub_history=admin_models.Subscription_History()
        sub_history.user=obj
        sub_history.subscription=plan[0]
        expire=datetime.datetime.now()+datetime.timedelta(days=6)
        sub_history.expire=expire
        sub_history.save()
        history=admin_models.Points_History()
        history.user=obj
        history.receive_track='Signup '+str(var1)+' Points'
        history.receive_track_name='App signup'
        history.save()
        #tools.send_sms('+'+request.POST['country_code']+request.POST['phone_number'],str(uzr.full_name)+' \n your OTP for Mayani \n'+str(uzr.otp)
        #  )
         
        try:
            
            tools.send_sms('+'+request.POST['country_code']+request.POST['phone_number'],str(uzr.full_name)+' \n your OTP for Mayani \n'+str(uzr.otp)
           )
        
        except Exception as e:
             return Response({'success':'false',
                                 'error_msg':str(e),
                                 'errors':'',
                                 'response':{},
                                 },status=status.HTTP_200_OK)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':serializers.user_data(uzr).data,
                            },status=status.HTTP_200_OK)
class check_user_otp(APIView):
    def get(self,request):
        # f0=serializers.password()
        f1=serializers.check_user_otp()

        return Response({**f1.data,
                            },status=status.HTTP_200_OK)
    def post(self,request):
        f1=serializers.check_user_otp(data=request.POST)
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':tools.beautify_errors({**dict(f1.errors)}),
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_200_OK)
        uzr=list(accounts_models.Users.objects.filter(id=request.POST['id']))
        if uzr==[]:
            return Response({'success':'false',
                                'error_msg':'invalid id',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
        uzr=uzr[0]
        if uzr.otp==request.POST["otp"]:
            uzr.is_varified=True
            uzr.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':serializers.user_data(uzr).data,
                                },status=status.HTTP_200_OK)
        else:
            return Response({'success':'false',
                                'error_msg':'invalid OTP',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
class create_password(APIView):
    def get(self,request):
        # f0=serializers.password()
        f1=serializers.create_password()
        return Response({**f1.data,
                            },status=status.HTTP_200_OK)
    def post(self,request):
        f1=serializers.create_password(data=request.POST)
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':tools.beautify_errors({**dict(f1.errors)}),
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_200_OK)
        if request.POST["password"]!=request.POST["confirm_password"]:
            return Response({'success':'false',
                                'error_msg':'Confirm password does not match',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
        uzr=list(accounts_models.Users.objects.filter(id=request.POST['id']))
        if uzr==[]:
            return Response({'success':'false',
                                'error_msg':'invalid id',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
        uzr=uzr[0]
        password=request.POST['password'].encode('utf-8')
        uzr.password=bcrypt.hashpw(password,bcrypt.gensalt())
        uzr.password=uzr.password.decode("utf-8")
        uzr.is_varified=True
        uzr.save()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':serializers.user_data(uzr).data,
                            },status=status.HTTP_200_OK)
class signin_user(APIView):
    @login_not_required()
    def get(self,request):
        f1=serializers.signin_user()
        return Response(f1.data,status=status.HTTP_200_OK)
    @login_not_required()
    def post(self,request):
        f1=serializers.signin_user(data=request.data)
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':tools.beautify_errors({**dict(f1.errors)}),
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_200_OK)
        uzr=list(accounts_models.Users.objects.filter(Q(country_code=request.POST['country_code'])&Q(phone_number=request.POST['phone_number'])))
        print("user",uzr)
        if uzr==[]:
            return Response({'success':'false',
                                'error_msg':'invalid credentials',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
        uzr=uzr[0]
        if uzr.is_varified==True:
            password=str(request.POST['password']).encode('utf-8')
            hash_pass=uzr.password.encode('utf-8')
            if bcrypt.checkpw(password,hash_pass):
                sec=''
                for i in range(10):
                    sec+=secrets.choice(secrets.choice([chr(ii) for ii in range(45,123)]))

                uzr.token=sec
                uzr.last_login=datetime.datetime.now()
                uzr.save()
                re=login_user(uzr.id,token=sec)
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{'user':[serializers.user_data(uzr).data],},
                                    'token':re,
                                },status=status.HTTP_200_OK)
            return Response({'success':'false',
                                'error_msg':'invalid credentials',
                                'response':{},
                                'errors':'',
                                },status=status.HTTP_200_OK)
        return Response({'success':'false',
                                'error_msg':'You are not verified',
                                'response':{},
                                'errors':'',
                                },status=status.HTTP_200_OK)

class get_forgotpass_user_otp(APIView):
    def post(self,request):
        result=accounts_models.Users.objects.get(phone_number=request.POST['phone_number'])
        result.otp=random.randint(1000,9999)
        result.save()
        try:
            
            tools.send_sms('+91'+result.phone_number,str(result.full_name)+' \n your OTP for Mayani \n'+str(result.otp)
           )
        
        except Exception as e:
             return Response({'success':'false',
                                 'error_msg':str(e),
                                 'errors':'',
                                 'response':{},
                                 },status=status.HTTP_200_OK)
        return Response({'success':'true',
                                 'error_msg':'send successfully',
                                 'errors':'',
                                 'response':{'id':result.id},
                                 },status=status.HTTP_200_OK)

class resend_user_otp(APIView):
    def get(self,request,user_id):
        result=accounts_models.Users.objects.get(id=user_id)

        try:
            
            tools.send_sms('+91'+result.phone_number,str(result.full_name)+' \n your OTP for Mayani \n'+str(result.otp)
           )
        
        except Exception as e:
             return Response({'success':'false',
                                 'error_msg':str(e),
                                 'errors':'',
                                 'response':{},
                                 },status=status.HTTP_200_OK)
        return Response({'success':'true',
                                 'error_msg':'send successfully',
                                 'errors':'',
                                 'response':{},
                                 },status=status.HTTP_200_OK)
