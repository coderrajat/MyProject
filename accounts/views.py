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
                    return Response({'success':'false','error_msg':'USER IS LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                return Response({'success':'false','error_msg':'USER IS LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)

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
                    return Response({'success':'false','error_msg':'invalid token','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                if len(data)==4 and time>datetime.datetime.now():
                    uzr= tools.get_user(*data)
                    if uzr!=[]:
                        print('#########',uzr.token)
                        if uzr.token=='':
                            return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        return func(*args,**kwargs)
                    else:
                        return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                return Response({'success':'false','error_msg':'token expire','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'success':'false','error_msg':'no HTTP_AUTHORIZATION ','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            return func(*args,**kwargs)
        return wrapper
    return inner
def login_admin(userid,token=''):
    token=tools.codetoken(userid,type='admin',token=token)
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
            print(password,hash_pass)
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
        # f0=serializers.password()
        f1=serializers.signup_user()

        return Response({**f1.data,
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
                                    'error_msg':'user alrady exist',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_200_OK)
            else:
                uzr.delete()
        uzr=accounts_models.Users()
        uzr.country_code=request.POST["country_code"]
        uzr.phone_number=request.POST["phone_number"]
        ##
        print(uzr.country_code)
        print(uzr.phone_number)
        ##
        uzr.otp=random.randint(1000,9999)
        uzr.save()
        tools.send_sms('+'+request.POST['country_code']+request.POST['phone_number'],str(uzr.full_name)+' \n your OTP for Mayani \n'+str(uzr.otp)
           )
         
        try:
            
            tools.send_sms('+'+request.POST['country_code']+request.POST['phone_number'],str(uzr.full_name)+' \n your OTP for Mayani \n'+str(uzr.otp)
           )
        
         
        except Exception as e:
             return Response({'success':'false',
                                 'error_msg':'please try again later',
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
                                'error_msg':'password and confirm_password dose not match',
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
        if uzr.otp!=request.POST["otp"]:
            return Response({'success':'false',
                                'error_msg':'invalid OTP',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
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
        if uzr==[]:
            return Response({'success':'false',
                                'error_msg':'invalid credentials',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
        uzr=uzr[0]
        password=str(request.POST['password']).encode('utf-8')
        hash_pass=uzr.password.encode('utf-8')
        print(uzr.password)
        print(password,hash_pass)
        if bcrypt.checkpw(password,hash_pass):
            sec=''
            for i in range(10):
                sec+=secrets.choice(secrets.choice([chr(ii) for ii in range(45,123)]))

            uzr.token=sec
            uzr.last_login=datetime.datetime.now()
            uzr.save()
            re=login_admin(uzr.id,token=sec)
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


'''
#sonu users

class userall_data(APIView):
    #@is_authenticate()
    def get(self,request, id=None):
        try:
            if id is not None:
                stu = list(accounts_models.Users.objects.filter(id=id))
              
                if len(stu)==0:
                    return Response ({'success':'false',
                                        'error_msg':'User does not Exist',
                                        'errors':{},
                                        'response':{}
                                        },status=status.HTTP_400_BAD_REQUEST)
                serializer = serializers.user_data(stu[0])
                return Response({'success':'true',
                                        'error_msg':'',
                                        'errors':{''},
                                        'response':{"User_data":serializer.data},
                                        },status=status.HTTP_200_OK)

            stu = accounts_models.Users.objects.all()
            #stu = accounts_models.Users.objects.count()
            print('The Total Users is =',stu.count())
            #a=stu.count()
            serializer = serializers.user_data(stu,many =True)
            return Response({'success':'true',
                                        'error_msg':'',
                                        'errors':{''},
                                        'response':{"User_data":serializer.data},
                                        },status=status.HTTP_200_OK)
        except ValueError as ex:
            return Response ({'success':'false',
                                        'error_msg':'Please enter a integer value as ID',
                                        'errors':{},
                                        'response':{}
                                        },status=status.HTTP_400_BAD_REQUEST)



#
'''