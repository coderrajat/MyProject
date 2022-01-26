#from Mayani_Backend.admins.models import album
from os import name
#from typing_extensions import ParamSpecKwargs
from django.db.models.aggregates import Count
from django.shortcuts import render
from rest_framework.serializers import Serializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework import status
from django.db.models import Q, manager
from accounts.views import login_admin
from admins import models as admin_models
from accounts import models as account_models
from users import models as user_models
from django.utils import timezone


# Create your views here.
import bcrypt
from accounts import tools
import datetime
from . import serializers
from rest_framework import status

def is_authenticate(*Dargs,**Dkwargs):
    def inner(func):
        def wrapper(*args,**kwargs):

            if 'HTTP_AUTHORIZATION'in args[1].META :
                try:
                    data=tools.decodetoken(args[1].META['HTTP_AUTHORIZATION'])

                    time=datetime.datetime.strptime(data[2].split('.')[0],'%Y-%m-%d %H:%M:%S')
                except Exception as e:
                    # print(e)
                    return Response({'success':'false','error_msg':'invalid token','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)

                if len(data)==4 and time>datetime.datetime.now():
                    uzr= tools.get_user(*data)
                    if uzr!=[]:
                        if uzr.is_user_blocked :
                            return Response({'success':'false','error_msg':'USER BLOCKED','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        # try:#do user has authorization
                        #     kwg=uzr.authorize.__dict__
                        #
                        # except:
                        #     return Response({'success':'false','error_msg':'USER UNAUTHORIZED','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        #
                        # for  i in Dkwargs:#does all given permitions are present
                        #     if Dkwargs[i]!=kwg[i]:
                        #
                        #         return Response({'success':'false','error_msg':'USER UNAUTHORIZED','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                        #     else:
                        #         print('match ',i,kwg[i],Dkwargs[i])
                        return func(*args,**kwargs)
                    else:
                        return Response({'success':'false','error_msg':'USER NOT LOGGEDIN','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
                return Response({'success':'false','error_msg':'token expire','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({'success':'false','error_msg':'no HTTP_AUTHORIZATION ','errors':{},'response':{}},status=status.HTTP_401_UNAUTHORIZED)
        return wrapper
    return inner

# add cms and get cms
class cms(APIView):
    @is_authenticate()
    def get(self,request,name):
        content=list(admin_models.CMS.objects.filter(name=name))
        if content==[]:
            if name in ['about_us','legal_disclamer','t&s','privacy_policy','how_to_pay_via_mobile']:
                cms=admin_models.CMS()
                cms.name=name
                cms.save()
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{'data':serializers.csm_about_us_api(cms).data},
                                    },status=status.HTTP_200_OK)
            else:
                return Response({'success':'false',
                                    'error_msg':name+' is a invalid term or policy',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
        content=content[0]
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'data':serializers.csm_about_us_api(content).data},
                            },status=status.HTTP_200_OK)
    @is_authenticate()
    def post(self,request,name):
        content=list(admin_models.CMS.objects.filter(name=name))
        if content==[]:
            #if name in []:
            if name in ['about_us','legal_disclamer','t&s','privacy_policy','how_to_pay_via_mobile']:
                cms=admin_models.CMS()
                cms.name=name
                cms.content=request.POST['content']
                cms.save()
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{'data':serializers.csm_about_us_api(cms).data},
                                    },status=status.HTTP_200_OK)
            else:
                return Response({'success':'false',
                                    'error_msg':name+' is a invalid term or policy',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
        content=content[0]
        f1=serializers.csm_about_us_api(data=request.POST,instance=content)
        if f1.is_valid():

            content.content=request.POST['content']
            content.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{'data':serializers.csm_about_us_api(content).data},
                                },status=status.HTTP_200_OK)
        else:
            return Response({'success':'false',
                                'error_msg':'CMS_content not valid',
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

class Faq_section(APIView):
    @ is_authenticate()
    def get(self,request,pk=None):
        try:
            if pk is not None:

                fq=list(admin_models.faq.objects.filter(pk=pk))
                if fq==[]:
                    return Response({'success':'false',
                            'error_msg':"Data does not exist",
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_400_BAD_REQUEST) 
                fq2=serializers.faq_category(fq[0])
                return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{"FAQ_data":fq2.data}
                            },status=status.HTTP_200_OK)
                            
            fq=admin_models.faq.objects.all()
            fq2=serializers.faq_category(fq,many=True)
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{"FAQ_data":fq2.data}
                                },status=status.HTTP_200_OK)
            
        except ValueError as ex:
            return Response({'success':'false',
                                'error_msg':"please enter integer value for id",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
    @is_authenticate()
    def post(self, request):
        fq=serializers.faq_category(data=request.data)
        if fq.is_valid():
            fq.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_200_OK)
        return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(fq.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)

    @is_authenticate()    
    def put(self,request,pk):
        try:
            
            fq=list(admin_models.faq.objects.filter(pk=pk))
            if fq==[]:
                return Response({'success':'false',
                                'error_msg':"Data does not exists ",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
            fq1=serializers.faq_category(fq[0],data=request.data)
            if fq1.is_valid():
                fq1.save()
                return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_200_OK)
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(fq1.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            return Response({'success':'false',
                                'error_msg':"please enter the integer value for id",
                                'errors':{},
                                'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST)
    @is_authenticate()                         
    def delete(self,request,pk):
        try:
            fq=list(admin_models.faq.objects.filter(pk=pk))
            if fq==[]:
                return Response({'success':'false',
                            'error_msg':"Data does not exixts",
                            'errors':{},
                            'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
            
            fq[0].delete()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK)
        except ValueError as ex:
            return Response({'success':'false',
                                'error_msg':"please enter the integer value for id",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)

class image_settings(APIView):
    @is_authenticate()
    def get(self,request):
        ims=admin_models.image_settings.objects.get_or_create(id='1',defaults={'deafult_profile_pic': 'deafult_profile_pic.jpeg','default_parking_spot_pic': 'default_parking_spot_pic.jpeg'})[0]
        f1=serializers.image_settings(ims)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'result':f1.data},
                            },status=status.HTTP_200_OK)
    @is_authenticate()
    def post(self,request):
        ims=admin_models.image_settings.objects.get_or_create(id='1',defaults={'deafult_profile_pic': 'deafult_profile_pic.jpeg','default_parking_spot_pic': 'default_parking_spot_pic.jpeg'})[0]
        f1=serializers.image_settings_base64(data=request.POST)
        for i in request.POST.keys():
            if ';base64,'in request.POST[i]:
                dt=tools.get_base64_to_img(request.POST[i])
                getattr(ims, i).delete()
                getattr(ims, i).save(i+'.jpeg',dt[0],save=True)       
        return Response({'success':'true',
                    'error_msg':'in',
                    'errors':{},
                    'response':{},
                    },status=status.HTTP_200_OK)

class smtp_settings_api(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.smtp_settings_api(list(admin_models.SMTP_setting.objects.filter(id=1))[0])
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{**f1.data},
                            },status=status.HTTP_200_OK)
    @is_authenticate()
    def post(self,request):
        if request.method=='POST':
            smtp=list(admin_models.SMTP_setting.objects.filter(id=1))[0]
            f1=serializers.smtp_settings_api(instance=smtp,data=request.POST)
            if f1.is_valid():
                f1.save()
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_200_OK)
            else:
                return Response({'success':'false',
                                    'error_msg':'',
                                    'errors':{**dict(f1.errors)},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
                            
class social_media_settings(APIView):
    @is_authenticate()
    def get(self,request):
        sms=list(admin_models.social_media_settings.objects.filter(id=1))
        if sms==[]:
            sms=admin_models.social_media_settings()
            sms.save()
        else:        
            sms=sms[0]
        return Response({'success':'true',
                    'error_msg':'',
                    'errors':{},
                    'response':{'result':serializers.social_media_settings(sms).data},
                    },status=status.HTTP_200_OK)
              

                    
    @is_authenticate()
    def post(self,request):
        sms=list(admin_models.social_media_settings.objects.filter(id=1))
        if sms==[]:
            sms=admin_models.social_media_settings()
            sms.save()
        else:
            sms=sms[0]
        f1=serializers.social_media_settings(instance=sms,data=request.POST)
        if f1.is_valid():
            f1.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
        else:
            return Response({'success':'false',
                                    'error_msg':'',
                                    'errors':{**dict(f1.errors)},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)

class general_settings_api(APIView):
    @is_authenticate()
    def get(self, request):
        g_s = admin_models.general_settings.objects.get(id = 1)
        return Response({'data':serializers.general_settings_serializer(g_s).data,
                            },status=status.HTTP_200_OK)
    @is_authenticate()
    def post(self, request):
        f1=serializers.general_settings_serializer(data=request.POST)
        if f1.is_valid():
            g_s = admin_models.general_settings.objects.get(id = 1)
            f1.instance = g_s
            f1.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':'Successfull updated',
                                },status=status.HTTP_200_OK)

        else:
            f1.is_valid()
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)

class admin_profile(APIView):
    @is_authenticate()
    def get(self,request):
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        print("test",requstuser)
        f1=serializers.admin_info(requstuser)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':f1.data,
                            },status=status.HTTP_200_OK)
    @is_authenticate()
    def post(self,request):
        
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        print("test","data")
        requstuser=tools.get_user(*data)
        print("test",requstuser)
        f1=serializers.admin_form(instance=requstuser,data=request.POST)
        f1.is_valid()
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        
        x=(Q(country_code=request.data['country_code'])&Q(phone_number=request.data['phone_number']))&~Q(id=requstuser.id)
        subadmin=list(account_models.Admins.objects.filter(x))
        if subadmin!=[]:
            return Response({'success':'false',
                                'error_msg':'phone number already exists',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
     
        uzr=f1.save()
        if  'profile_pic' in request.FILES:
            if requstuser.profile_pic != 'deafult_profile_pic.jpeg':
                requstuser.profile_pic.delete()
            uzr.profile_pic=request.FILES['profile_pic']
        uzr.save()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},

                            },status=status.HTTP_200_OK)

class change_admin_password(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.change_password()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':f1.data,
                            },status=status.HTTP_200_OK)
    @is_authenticate()
    def post(self,request):
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        f1=serializers.change_password(data=request.POST)
        if f1.is_valid():

            if request.POST['password']=='':

                return Response({'success':'false',
                                    'error_msg':'',
                                    'errors':{'password':["Passwords should not empty"]},
                                    'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
            password=str(request.POST['oldpassword']).encode('utf-8')
            print("test",password)
            hash_pass=requstuser.password.encode('utf-8')
            print("test",requstuser.password)

            if bcrypt.checkpw(password,hash_pass):
                if request.POST['password']==request.POST['confirm_password']:
                    user=requstuser
                    password=request.POST['password'].encode('utf-8')
                    user.password=bcrypt.hashpw(password,bcrypt.gensalt())
                    user.password=user.password.decode("utf-8")
                    user.save()
                    return Response({'success':'true',
                                        'error_msg':'',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_200_OK)
                else:
                    return Response({'success':'false',
                                        'error_msg':'',
                                        'errors':{**dict(f1.errors),**{'confirm_password':["Confirm Password does not match"]}},
                                        'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'success':'false',
                                    'error_msg':'',
                                    'errors':{'oldpassword':["Old Password is incorrect"]},
                                    'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success':'false',
                                'error_msg':'',
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

class search_consumer_api(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.search_user()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    @is_authenticate()
    def post(self,request):
        f1=serializers.search_user(data=request.POST)
        f2=serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            f1.is_valid()
            f2.is_valid()
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors),**dict(f2.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        result_flg=True
        s=request.POST['search']
        search_query=Q()
        second_search_query=Q()
        if request.POST['subscription_plan']!='':
            second_search_query.add(Q(subscription_plan__icontains=request.POST['subscription_plan']),Q.AND)
            # result_flg=False
        if s!='':
            search_query.add(Q(email__icontains=s),Q.OR)
            search_query.add(Q(phone_number__icontains=s),Q.OR)
            search_query.add(Q(country_code__icontains=s),Q.OR)
            search_query.add(Q(full_name__icontains=s),Q.OR)
            search_query.add(Q(bio__icontains=s),Q.OR)
            # result_flg=False
        if result_flg:
            result=account_models.Users.objects.filter(second_search_query&search_query)
        else:
            result=account_models.Users.objects.all()
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
        paginate_result=Paginator(result, request.POST['result_limit'])
        p_r=paginate_result.get_page(request.POST['page'])
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'result':serializers.user_forms(p_r,many=True).data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                                },
                            },status=status.HTTP_202_ACCEPTED)

class edit_user_api(APIView):
    @is_authenticate()
    def get(self,request,id):
        user=list(account_models.Users.objects.filter(id=id))
        if user==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        user=user[0] 
        f1=serializers.search_consumer_form(user)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':f1.data,
                            },status=status.HTTP_200_OK)
    
    

    @is_authenticate()
    def post(self,request,id=None):
        try:
            #data = request.POST
            user=list(account_models.Users.objects.filter((Q(country_code=request.data['country_code'])&Q(phone_number=request.data['phone_number']))))
            if user!=[]:
                return Response({'success':'false',
                                        'error_msg':'phone number already exists',
                                        'errors':{},
                                        'response':{}
                                        },status=status.HTTP_406_NOT_ACCEPTABLE)
            serializer =  serializers.user_forms(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({'Success':'true',
                                        'error_msg':'',
                                        'errors':{},
                                        'response':{""},
                                        },status=status.HTTP_200_OK)
            return Response({'success':'false',
                                        'error_msg':'invalid_input',
                                        'errors':{},
                                        'response':{**dict(serializer.errors)}
                                        },status=status.HTTP_406_NOT_ACCEPTABLE)
        except ValueError as ex:
            return Response ({'success':'false',
                                        'error_msg':'Please enter a integer value as ID',
                                        'errors':{},
                                        'response':{}
                                        },status=status.HTTP_406_NOT_ACCEPTABLE)
                              
    @is_authenticate()
    def put(self,request,id):
        user=list(account_models.Users.objects.filter(id=id))
        
        

        if user==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

       
        #f1=serializers.user_forms(instance=user,data=request.POST)
        
        
        user=user[0]
          
        f1=serializers.edit_user_forms(instance=user,data=request.data)
        x=(Q(country_code=request.data['country_code'])&Q(phone_number=request.data['phone_number']))&~Q(id=id)
        uzr=list(account_models.Users.objects.filter(x))
        
        if uzr!=[]:
            return Response ({'success':'false',
                                        'error_msg':'phone number already exists',
                                        'errors':{},
                                        'response':{}
                                        },status=status.HTTP_406_NOT_ACCEPTABLE) 
        #f1.is_valid()
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        uzr=f1.save()
        if  'profile_pic' in request.FILES:
            if user.profile_pic != 'deafult_profile_pic.jpeg':
                user.profile_pic.delete()
            uzr.profile_pic=request.FILES['profile_pic']
        uzr.save()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},

                            },status=status.HTTP_200_OK)
        

class delete_user(APIView):
    @is_authenticate()
    def delete(self,request,id):
        user=list(account_models.Users.objects.filter(id=id))
        if user==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        user=user[0]
        try:
            if user.profile_pic != 'deafult_profile_pic.jpeg':
                user.profile_pic.delete()
            user.delete()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
        except:
            return Response({'success':'false',
                                'error_msg':'',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
                               
class block_user(APIView):
    @is_authenticate()
    def get(self,request,id):
        user=list(account_models.Users.objects.filter(id=id))
        if user==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        user=user[0]

        user.is_user_blocked=not user.is_user_blocked
        user.save()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK)

class subadmin_list(APIView):
    @is_authenticate()
    def post(self,request):
        f1=serializers.pagination(data=request.POST)
        f2 = serializers.search(data=request.POST)

        if not(f1.is_valid() ):
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)

        s=request.POST['search']
        search_query=Q()
        search_query.add(~Q(id=requstuser.id),Q.AND)
        if s!='':
            search_query.add(Q(first_name__icontains=s) | Q(last_name__icontains=s) | Q(email__icontains=s),Q.AND)


        result=list(account_models.Admins.objects.filter(search_query))
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
        paginate_result=Paginator(result, request.POST['result_limit'])
        p_r=paginate_result.get_page(request.POST['page'])
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'result':serializers.admin_data(p_r,many=True).data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                                },
                            },status=status.HTTP_202_ACCEPTED)

class edit_subadmin(APIView):
    @is_authenticate()
    def get(self,request,id):
        user=list(account_models.Admins.objects.filter(id=id))
        if user==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        user=user[0]
        f1=serializers.admin_data(user)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':f1.data,
                            },status=status.HTTP_200_OK)
    @is_authenticate()
    def post(self,request,id):
        user=list(account_models.Admins.objects.filter(id=id))
        x=(Q(country_code=request.data['country_code'])&Q(phone_number=request.data['phone_number']))&~Q(id=id)
        subadmin=list(account_models.Admins.objects.filter(x))

        if user==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        user=user[0]
        if subadmin!=[]:
            return Response({'success':'false',
                                'error_msg':'phone number already exist',
                                'errors':'',
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST) 
        f1=serializers.admin_form(instance=user,data=request.POST)
        f1.is_valid()
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        uzr=f1.save()
        if  'profile_pic' in request.FILES:
            if uzr.profile_pic != 'deafult_profile_pic.jpeg':
               uzr.profile_pic.delete()
            uzr.profile_pic=request.FILES['profile_pic']
        uzr.save()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},

                            },status=status.HTTP_200_OK)

class delete_subadmin(APIView):
    @is_authenticate()
    def delete(self,request,id):
        user=list(account_models.Admins.objects.filter(id=id))
        if user==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        user=user[0]
        try:
            
            if user.profile_pic != 'deafult_profile_pic.jpeg':
                user.profile_pic.delete()
            user.delete()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
        except:
            return Response({'success':'false',
                                'error_msg':'',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
    
class block_subadmin(APIView):
    @is_authenticate()
    def get(self,request,id):
        user=list(account_models.Admins.objects.filter(id=id))
        if user==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        user=user[0]

        user.is_user_blocked=not user.is_user_blocked
        user.save()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                           },status=status.HTTP_200_OK)
class Add_Subadmin(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.admin_form()
        return Response(f1.data)
    @is_authenticate()
    def post(self,request):
      f1=serializers.admin_form(data=request.data)
      if not ( f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':tools.beautify_errors({**dict(f1.errors)}),
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_200_OK)
      subadmin=list(account_models.Admins.objects.filter((Q(country_code=request.data['country_code'])&Q(phone_number=request.data['phone_number']))))
      if subadmin==[]:
        subadmin=f1.save()
        if  'profile_pic' in request.FILES:
            subadmin.profile_pic=request.FILES['profile_pic']
            subadmin.save()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':serializers.admin_form(subadmin).data,
                            },status=status.HTTP_200_OK)   
      return Response({'success':'false',
                                 'error_msg':'phone number already exists',
                                 'errors':'',
                                 'response':{},
                                 },status=status.HTTP_400_BAD_REQUEST)   
     
                                

#---- Genere APIs ------
class Genere_API(APIView):
    @is_authenticate()
    def get(self, request, id):
        if(id == '-1'):
            data = admin_models.Generes.objects.all()

            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{"data": serializers.Genere_Serializer(data, many=True).data},
                            },status=status.HTTP_200_OK)  

        if(not id.isnumeric()):
            return Response({'success':'false',
                                 'error_msg':'Invalid id',
                                 'errors':'',
                                 'response':{},
                                 },status=status.HTTP_400_BAD_REQUEST)

        data = list(admin_models.Generes.objects.filter(id=id))
        if(data == []):
            return Response({'success':'false',
                                 'error_msg':'Genre not found',
                                 'errors':'',
                                 'response':{},
                                 },status=status.HTTP_404_NOT_FOUND)
        
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{"data": serializers.Genere_Serializer(data[0]).data},
                            },status=status.HTTP_200_OK) 
    @is_authenticate()
    def post(self, request, id):
        f1 = serializers.Genere_Serializer(data=request.POST)
        if f1.is_valid():
            f1.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK)
        else:
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)


    @is_authenticate()
    def put(self, request, id):

        if(not id.isnumeric()):
            return Response({'success':'false',
                                 'error_msg':'Invalid id',
                                 'errors':'',
                                 'response':{},
                                 },status=status.HTTP_400_BAD_REQUEST)

        data = list(admin_models.Generes.objects.filter(id=id))
        if(data == []):
            return Response({'success':'false',
                                 'error_msg':'Genre not found',
                                 'errors':'',
                                 'response':{},
                                 },status=status.HTTP_404_NOT_FOUND)


        f1 = serializers.Genere_Serializer(data=request.data, instance=data[0])
        if f1.is_valid():
            f1.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK)
        else:
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)
    
    @is_authenticate()
    def delete(self, request, id):

        if(not id.isnumeric()):
            return Response({'success':'false',
                                 'error_msg':'Invalid id',
                                 'errors':'',
                                 'response':{},
                                 },status=status.HTTP_400_BAD_REQUEST)

        data = list(admin_models.Generes.objects.filter(id=id))
        if(data == []):
            return Response({'success':'false',
                                 'error_msg':'Genre not found',
                                 'errors':'',
                                 'response':{},
                                 },status=status.HTTP_404_NOT_FOUND)

        data[0].delete()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK)
#-------

             
#---- Recommendations by Admin APIS -------
class Admin_Recommendations(APIView):
    @is_authenticate()
    def post(self, request):
        f1 = serializers.Add_recommended_song_serializer(data=request.data)
        if not f1.is_valid():
            return Response({'success':'false',
                            'error_msg':'invalid_input',
                            'errors':{},
                            'response':{**dict(f1.errors)}
                            },status=status.HTTP_400_BAD_REQUEST)
        
        user = list(account_models.Users.objects.filter(id=request.data["user_id"]))

        if(user == []):
            return Response({'success':'false',
                            'error_msg':'user does not exist',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_404_NOT_FOUND)
        
        song = list(admin_models.songs.objects.filter(id=request.data["song_id"]))

        if(song == []):
            return Response({'success':'false',
                            'error_msg':'song does not exist',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_404_NOT_FOUND)
        user = user[0]
        song = song[0]

        recommendations = list(user_models.Recommended_Songs_by_admin.objects.filter(user=user))

        if recommendations == []:
            recommendations = user_models.Recommended_Songs_by_admin()
            recommendations.user = user
            recommendations.save()
        else:
            recommendations = recommendations[0]
        
        recommendations.songs.add(song)
        recommendations.save()

        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK) 
    
    @is_authenticate()
    def delete(self, request):
        f1 = serializers.Add_recommended_song_serializer(data=request.data)
        if not f1.is_valid():
            return Response({'success':'false',
                            'error_msg':'invalid_input',
                            'errors':{},
                            'response':{**dict(f1.errors)}
                            },status=status.HTTP_400_BAD_REQUEST)
        
        user = list(account_models.Users.objects.filter(id=request.data["user_id"]))

        if(user == []):
            return Response({'success':'false',
                            'error_msg':'user does not exist',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_404_NOT_FOUND)
        
        song = list(admin_models.songs.objects.filter(id=request.data["song_id"]))

        if(song == []):
            return Response({'success':'false',
                            'error_msg':'song does not exist',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_404_NOT_FOUND)
        user = user[0]
        song = song[0]

        recommendations = list(user_models.Recommended_Songs_by_admin.objects.filter(user=user))

        if recommendations == []:
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK) 
        else:
            recommendations = recommendations[0]
        
        recommendations.songs.remove(song)
        recommendations.save()

        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK) 

class Search_Recommended_Songs(APIView):
    @is_authenticate()                     
    def post(self,request,id):
        f1=serializers.search(data=request.POST)
        f2=serializers.pagination(data=request.POST)
        #print("serializer",f1,f2)
        if not(f1.is_valid() and f2.is_valid()):
            f1.is_valid()
            f2.is_valid()
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors),**dict(f2.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        s=request.POST['search']
        
        flg=True
        search_query=Q()
        print("-----", id)
        search_query.add(Q(recommended_to_user__user__id=id), Q.AND)
        if s!='':
            flg=False
              
            search_query.add(Q(name__icontains=s) | Q(album__name__icontains=s) | Q(artist__name__icontains=s),Q.AND)
            #search_query.add(Q(charts__icontains=s),Q.OR)
            #result=admin_models.songs.objects.select_related.filter(Q(name__icontains=s)

       
        result=admin_models.songs.objects.filter(search_query).distinct().order_by('-id')
        #print('\n\n#result=',result[0].album.__dict__,result[0].album.year,'\n\n')
        """
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
        """
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        # print(p_r)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'result':serializers.song_data(p_r,many=True).data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                                },
                            },status=status.HTTP_202_ACCEPTED)  
           
    
        







#------  SONG APIS ------

# Song Add, Edit, Delete, View
class Song_api(APIView):
    @is_authenticate()
    def get(self, request,pk=None):
        if(pk.isnumeric()):
            song=list(admin_models.songs.objects.filter(pk=pk))
            if song==[]:
                return Response({'success':'false',
                        'error_msg':"Data not exists in database",
                        'errors':{},
                        'response':{}
                        },status=status.HTTP_400_BAD_REQUEST) 
            f1=serializers.Song_data(song[0])     

            return Response({'success':'true',
                        'error_msg':'',
                        'errors':{},
                        'response':{"song":f1.data}
                        },status=status.HTTP_200_OK)
            
        else:
            return Response({'success':'false',
                                'error_msg':"please enter integer value for id",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
    @is_authenticate()
    def post(self, request):
        f2=serializers.Add_song_serializer(data=request.data)
        if f2.is_valid():
            file=request.FILES.get('song_mp3', False)
            if  not file or not file.content_type  in ["audio/mpeg"]:
                return Response({'success':'false',
                                    'error_msg':'invalid file type,it should be mp3/mpeg',
                                    'errors':{},
                                    'response':{**dict(f2.errors)}
                                    },status=status.HTTP_400_BAD_REQUEST)
            song=f2.save()
            song.song_mp3=file

            try:
                if(request.data['artist'] != ""):
                    for i in request.data['artist'].split(","):
                        a = admin_models.artist.objects.get(pk=int(i))
                        song.artist.add(i)

                """
                if(request.data['admin_playlist'] != ""):
                    for i in request.data['admin_playlist'].split(","):
                        a = admin_models.playlist_admin.objects.get(pk=int(i))
                        song.admin_playlist.add(i)
                """
                
            
            except Exception as e:
                return Response({'success':'false',
                                        'error_msg':'The ID given are not real',
                                        'errors':{},
                                        'response':{}
                                        },status=status.HTTP_400_BAD_REQUEST)
            
            
            song.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_200_OK)
        return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f2.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)
    @is_authenticate()    
    def put(self,request,pk):
        if(pk.isnumeric()):
            song=list(admin_models.songs.objects.filter(pk=pk))
            if song==[]:
                return Response({'success':'false',
                                'error_msg':"Data not exists in database",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
            
                
            
            f1=serializers.Add_song_serializer(song[0],data=request.data)

            
            if f1.is_valid():
                song=f1.save()
                try:
                    if(request.data['artist'] != ""):
                        song.artist.clear()
                        for i in request.data['artist'].split(","):
                            a = admin_models.artist.objects.get(pk=int(i))
                            song.artist.add(i)
                    else:
                        song.artist.clear()

                    """
                    if(request.data['admin_playlist'] != ""):
                        song.admin_playlist.clear()
                        for i in request.data['admin_playlist'].split(","):
                            a = admin_models.playlist_admin.objects.get(pk=int(i))
                            song.admin_playlist.add(i)
                        
                        print("print", admin_models.playlist_admin.objects.filter(songs=song.id))
                        for j in admin_models.playlist_admin.objects.filter(songs=song.id):
                            print("here")
                            if(str(j.id) not in request.data['admin_playlist'].split(",")):
                                j.songs.remove(song.id)
                                j.save()
                    else:
                        for j in admin_models.playlist_admin.objects.filter(songs=song.id):
                            if(str(j.id) not in request.data['admin_playlist'].split(",")):
                                j.songs.remove(song.id)
                                j.save()
                    """
                    if  request.FILES.get('song_mp3', False) and (not request.FILES.get('song_mp3', False).content_type  in ["audio/mpeg"]):
                        return Response({'success':'false',
                                            'error_msg':'invalid file type,it should be mp3/mpeg',
                                            'errors':{},
                                            'response':{}
                                            },status=status.HTTP_400_BAD_REQUEST)
                    elif request.FILES.get('song_mp3', False):
                        song.song_mp3=request.FILES.get('song_mp3', False)
                    
                    song.save()

                except Exception as e:
                    return Response({'success':'false',
                                            'error_msg':'The ID given are not real',
                                            'errors':{},
                                            'response':{}
                                            },status=status.HTTP_400_BAD_REQUEST)


                return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_200_OK)
            
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)

        else:
            return Response({'success':'false',
                                'error_msg':"please enter the integer value for id",
                                'errors':{},
                                'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST)
        
        
        
    @is_authenticate()                         
    def delete(self,request,pk):

        if(pk.isnumeric()):
            song=list(admin_models.songs.objects.filter(pk=pk))
            if song==[]:
                return Response({'success':'false',
                                'error_msg':"Data not exists in database",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
            
            if song[0].cover != 'deafult_profile_pic.jpeg':
                song[0].cover.delete()
            song[0].song_mp3.delete()
            song[0].delete()

            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK)

        else:
            return Response({'success':'false',
                                'error_msg':"please enter the integer value for id",
                                'errors':{},
                                'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST)
# Song Search API   
class song_search_list(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)

    @is_authenticate()                     
    def post(self,request):
        f1=serializers.search(data=request.POST)
        f2=serializers.pagination(data=request.POST)
        #print("serializer",f1,f2)
        if not(f1.is_valid() and f2.is_valid()):
            f1.is_valid()
            f2.is_valid()
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors),**dict(f2.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        s=request.POST['search']
        
        flg=True
        if s!='':
            flg=False
            search_query=Q()  
            search_query.add(Q(name__icontains=s) | Q(album__name__icontains=s) | Q(artist__name__icontains=s),Q.AND)
            #search_query.add(Q(charts__icontains=s),Q.OR)
            #result=admin_models.songs.objects.select_related.filter(Q(name__icontains=s)

        if flg:
            result=admin_models.songs.objects.select_related().order_by('-id')
        else:
            result=admin_models.songs.objects.filter(search_query).distinct().order_by('-id')
        #print('\n\n#result=',result[0].album.__dict__,result[0].album.year,'\n\n')
        """
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
        """
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        # print(p_r)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'result':serializers.song_data(p_r,many=True).data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                                },
                            },status=status.HTTP_202_ACCEPTED)




#----- PLAYLIST APIs ------

#searching for specific playlist
class get_playlist_admin(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)

    @is_authenticate()                           
    def post(self,request):
        f1=serializers.search(data=request.POST)
        f2=serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            f1.is_valid()
            f2.is_valid()
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors),**dict(f2.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        s=request.POST['search']
        flg=True
        if s!='':
            flg=False
            search_query=Q()
            search_query.add(Q(name__icontains=s) | Q(gener__name__icontains=s),Q.AND)
        if flg:
            result=admin_models.playlist_admin.objects.select_related()
        else:
            result=admin_models.playlist_admin.objects.select_related().filter(search_query)
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        #print(p_r)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'result':serializers.playlist_admin_data(p_r,many=True).data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                                },
                            },status=status.HTTP_202_ACCEPTED)

# Search songs in a playlist
class get_song_admin_playlist(APIView):
    @is_authenticate()
    def get(self,request,id):
        f1=serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)

    @is_authenticate()                          
    def post(self,request,id):
        if not id.isnumeric():
            return Response({'success':'false',
                                'error_msg':'playlist id does not exist',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

        playlist_check=list(admin_models.playlist_admin.objects.filter(id=id))
        if len(playlist_check)==0:
            return Response({'success':'false',
                                'error_msg':'playlist id does not exist',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)                  
        f1=serializers.search(data=request.POST)
        f2=serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            f1.is_valid()
            f2.is_valid()
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors),**dict(f2.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        s=request.POST['search']
        flg=True
        if s!='':
            flg=False
            search_query=Q()
            search_query.add(Q(name__icontains=s) | Q(genres__name__icontains=s),Q.AND)
        if flg:
            result=admin_models.songs.objects.filter(admin_playlist=playlist_check[0].id)
        else:
            result=admin_models.songs.objects.filter(search_query,admin_playlist=playlist_check[0].id)
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        #print(p_r)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'playlist_name':playlist_check[0].name, 'result':serializers.song_data(p_r,many=True).data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                                },
                            },status=status.HTTP_202_ACCEPTED)

# Playlist edit, delete, View
class playlist_admin(APIView):
    @is_authenticate()
    def get(self,request,id):
        if id.isnumeric() !=  True:
            return Response({'success':'false',
                            'error_msg':'ID IS NOT AN INTEGER',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_404_NOT_FOUND)

        playlist=list(admin_models.playlist_admin.objects.prefetch_related().filter(id=id))
        print(playlist)

        if playlist==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        playlist=playlist[0]
        f1=serializers.playlist_admin_data(playlist)

        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{"playlist_data":f1.data},#"songs":serializers.song_data(playlist.songs.all(),many=True).data
                            },status=status.HTTP_200_OK)
    @is_authenticate()
    def put(self,request,id):
        f=request.data
        print(f)
        if id.isnumeric() !=  True:
            return Response({'success':'false',
                            'error_msg':'ID IS NOT AN INTEGER',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_404_NOT_FOUND)
        playlist=list(admin_models.playlist_admin.objects.filter(id=id))
        if playlist==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        playlist=playlist[0]
                        

        
        f1=serializers.playlist_admin_form(data=request.data,instance=playlist)
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)
        f1.save()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK)
    

    @is_authenticate()
    def delete(self, request, id):
        if id.isnumeric() !=  True:
            return Response({'success':'false',
                            'error_msg':'ID IS NOT AN INTEGER',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_404_NOT_FOUND)

        
        snippet = admin_models.playlist_admin.objects.filter(id=id)
        if len(snippet)==0:
            return Response({'success':'false',
                                'error_msg':'ID NOT FOUND',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_204_NO_CONTENT)
            
            
        f1=serializers.playlist_admin_form(snippet[0])
        print(f1.data)
        snippet[0].delete()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{"deleted":{**dict(f1.data)}},
                            },status=status.HTTP_200_OK)

# Remove a song from playlist
class playlist_admin_removesong(APIView):
    @is_authenticate()
    def post(self,request,id):
        try:
            temp=list(admin_models.playlist_admin.objects.filter(id=id))
            
            delete_id=request.data['delete_id']
            #print(delete_id)

            
            for i in temp:
                pass
            #print(i)
            j=i.songs.all()
           
            j_id=j.get(id=delete_id)
            i.songs.remove(j_id)
            i.save()
            
        except Exception as e:
            return Response({'success':'false',
                                'error_msg':'ID error',
                                'errors':{},
                                'response':{'all_playlist':''}
                                },status=status.HTTP_200_OK)
        
        return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{'all_playlist':serializers.playlist_admin_form(i).data}
                                },status=status.HTTP_200_OK)

# add a song to playlist
class playlist_admin_addsong(APIView):
    @is_authenticate()
    def post(self,request,id):
        
        try:
            temp=list(admin_models.playlist_admin.objects.filter(id=id))
            
          
            
            song_id=request.data['add_song']
            temp2=list(admin_models.songs.objects.filter(id=song_id))
            add_song_id=temp2[0]
            #print(temp2[0])
            #print(song_id)
            #print(delete_id)

            
            for i in temp:
                pass
            j=i.songs.all()
           
           
            #j_id=j.get(id=song_id)
            i.songs.add(add_song_id)
            i.save()
            
        except Exception as e:
            return Response({'success':'false',
                                'error_msg':'ID error',
                                'errors':{},
                                'response':{'all_playlist':''}
                                },status=status.HTTP_200_OK)
        
        return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{'all_playlist':serializers.playlist_admin_form(i).data}
                                },status=status.HTTP_200_OK)

# Playlist Add 
class playlist_admin_get(APIView): 
    @is_authenticate()
    def get(self,request):
        temp=admin_models.playlist_admin.objects.all()
        f1=serializers.playlist_admin_form(temp,many=True)
        return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{'all_playlist':f1.data}
                                },status=status.HTTP_200_OK)


    @is_authenticate()
    def post(self,request):
        f1=serializers.playlist_admin_form(data=request.data)
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)
        f1.save()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK)


#----- CHARTS APIs -------
# Charts Add 
class Charts_API(APIView): 
    @is_authenticate()
    def get(self,request,id):
        if id == "-1":
            chart=list(admin_models.charts_admin.objects.all())
            f1=serializers.Get_Charts_Serializer(chart, many=True)

            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{"chart_data":f1.data},#"songs":serializers.song_data(playlist.songs.all(),many=True).data
                            },status=status.HTTP_200_OK)

        if id.isnumeric() !=  True:
            return Response({'success':'false',
                            'error_msg':'ID IS NOT AN INTEGER',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_404_NOT_FOUND)

        chart=list(admin_models.charts_admin.objects.prefetch_related().filter(id=id))
        print(chart)

        if chart==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        chart=chart[0]
        f1=serializers.Get_Charts_Serializer(chart)

        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{"chart_data":f1.data},#"songs":serializers.song_data(playlist.songs.all(),many=True).data
                            },status=status.HTTP_200_OK)
    
    @is_authenticate()
    def post(self,request, id):
        f1=serializers.Charts_Serializer(data=request.data)
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)
        chart=f1.save()
        if  'cover' in request.FILES:
            chart.cover=request.FILES['cover']
            chart.save()

        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK)

    @is_authenticate()
    def put(self,request, id):
        if id.isnumeric() !=  True:
            return Response({'success':'false',
                            'error_msg':'ID IS NOT AN INTEGER',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_404_NOT_FOUND)
        chart = admin_models.charts_admin.objects.filter(id=id)

        if chart == []: 
            return Response({'success':'false',
                            'error_msg':'chart not found',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_404_NOT_FOUND)                   

        f1=serializers.Charts_Serializer(data=request.data, instance=chart[0])
        print("-----",request.data['gener'])
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)
        chart = f1.save()
        if  'cover' in request.FILES:
            if chart.cover != 'deafult_profile_pic.jpeg':
                chart.cover.delete()

            chart.cover=request.FILES['cover']
            chart.save()

        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK)

    @is_authenticate()
    def delete(self,request, id):
        if id.isnumeric() !=  True:
            return Response({'success':'false',
                            'error_msg':'ID IS NOT AN INTEGER',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_404_NOT_FOUND)
        chart = admin_models.charts_admin.objects.filter(id=id)

        if chart == []: 
            return Response({'success':'false',
                            'error_msg':'chart not found',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_404_NOT_FOUND)                   

        chart = chart[0]

        if chart.cover != 'deafult_profile_pic.jpeg':
            chart.cover.delete()

        chart.delete()

        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK)

class Add_Songs_to_Charts(APIView):
    @is_authenticate()
    def post(self,request):
        try:
            song=admin_models.songs.objects.get(pk=int(request.POST["song_id"]))
            chart=admin_models.charts_admin.objects.get(pk=int(request.POST["chart_id"]))
           

            
            chart.songs.add(song)
            chart.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK)
        
        except  Exception as ex:
            return Response({'success':'false',
                                'error_msg':"chart or song does not exists",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)

    @is_authenticate()
    def put(self,request):
        try:
            song=admin_models.songs.objects.get(pk=int(request.POST["song_id"]))
            chart=admin_models.charts_admin.objects.get(pk=int(request.POST["chart_id"]))
            
            chart.songs.remove(song)
            chart.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'success':'false',
                                'error_msg':"chart or song does not exists",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)



#----- ARTIST APIS ------

# Artist Add, Edit, View, Delete
class Artist_api(APIView):
    @is_authenticate()
    def get(self, request,pk=None):
        if(pk.isnumeric()):
            artist=list(admin_models.artist.objects.filter(pk=pk))
            if artist==[]:
                return Response({'success':'false',
                        'error_msg':"Data not exists in database",
                        'errors':{},
                        'response':{}
                        },status=status.HTTP_400_BAD_REQUEST) 
            f1=serializers.Artist_data(artist[0])     

            return Response({'success':'true',
                        'error_msg':'',
                        'errors':{},
                        'response':{"artist_data":f1.data}
                        },status=status.HTTP_200_OK)
            
        else:
            return Response({'success':'false',
                                'error_msg':"please enter integer value for id",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
    @is_authenticate()
    def post(self, request):
        f2=serializers.Add_artist_serializer(data=request.data)
        if f2.is_valid():
            f2.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_200_OK)
        return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f2.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)
    @is_authenticate()    
    def put(self,request,pk):
        if(pk.isnumeric()):
            artist=list(admin_models.artist.objects.filter(pk=pk))
            if artist==[]:
                return Response({'success':'false',
                                'error_msg':"Data not exists in database",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
            f1=serializers.Add_artist_serializer(artist[0],data=request.data)
            if f1.is_valid():
                f1.save()
                return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_200_OK)

        else:
            return Response({'success':'false',
                                'error_msg':"please enter the integer value for id",
                                'errors':{},
                                'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST)
        
        
        
    @is_authenticate()                         
    def delete(self,request,pk):

        if(pk.isnumeric()):
            artist=list(admin_models.artist.objects.filter(pk=pk))
            if artist==[]:
                return Response({'success':'false',
                                'error_msg':"Data not exists in database",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
            song=admin_models.songs.objects.filter(artist__pk=pk)
            for sg in song:
                sg.artist.remove(pk)
                sg.save()
            artist[0].delete()

            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK)

        else:
            return Response({'success':'false',
                                'error_msg':"please enter the integer value for id",
                                'errors':{},
                                'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST)
     
# Search Artist API
class Artist_search_list(APIView):
    @is_authenticate()
    def get(self, request):
        f1=serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    @is_authenticate()
    def post(self, request):
        f1=serializers.search(data=request.POST)
        f2=serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            f1.is_valid()
            f2.is_valid()
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors),**dict(f2.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        s=request.POST['search']
        flg=True
        if s!='':
            flg=False
            search_query=Q()
            search_query.add(Q(name__icontains=s) | Q(artist_origin__icontains=s),Q.AND)
        if flg:
            result=admin_models.artist.objects.select_related().distinct().order_by('-id')
        else:
            result=admin_models.artist.objects.select_related().filter(search_query).distinct().order_by('-id')
        
        """
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
        """
        
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        

        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'result':serializers.Artist_data(p_r,many=True).data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                                },
                            },status=status.HTTP_202_ACCEPTED)

# Search Albums in Artist
class Artist_album_search_list(APIView):
    @is_authenticate()
    def get(self, request):
        f1=serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    @is_authenticate()
    def post(self, request,pk):
            try:
                id=pk
                artist=admin_models.artist.objects.filter(pk=id)
                if len(artist)==0:
                    return Response({'success':'false',
                                        'error_msg':"Artist does not exists",
                                        'errors':{},
                                        'response':{}
                                        },status=status.HTTP_400_BAD_REQUEST)
                
                f1=serializers.search(data=request.POST)
                f2=serializers.pagination(data=request.POST)
                if not(f1.is_valid() and f2.is_valid()):
                    f1.is_valid()
                    f2.is_valid()
                
                    return Response({'success':'false',
                                        'error_msg':'invalid_input',
                                        'errors':{},
                                        'response':{**dict(f1.errors),**dict(f2.errors)},
                                        },status=status.HTTP_400_BAD_REQUEST)
                s=request.POST['search']
            
                search_query=Q()
                search_query.add(Q(songs__artist__id=id), Q.AND)
                if s!='':
                    search_query.add(Q(name__icontains=s),Q.AND)
                
                
                
                result=admin_models.album.objects.filter(search_query).distinct().order_by('-id')
                
                """
                if request.POST['order_by']!=None and request.POST['order_by']!='':
                    if request.POST['order_by_type']=='dec':
                        order='-'+request.POST['order_by']
                    else:
                        order=request.POST['order_by']
                    result=result.order_by(order)
                """
                
                paginate_result=Paginator(result, int(request.POST['result_limit']))
                p_r=paginate_result.get_page(request.POST['page'])
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{'artist_name':artist[0].name, 'result':serializers.Album_data(p_r,many=True).data},
                                    'pagination':{'count':len(list(p_r)),
                                                'previous':'true' if p_r.has_previous() else 'false',
                                                'next':'true' if p_r.has_next() else 'false',
                                                'startIndex':p_r.start_index(),
                                                'endIndex':p_r.end_index(),
                                                'totalResults':len(list(result)),
                                        },
                                    },status=status.HTTP_202_ACCEPTED)
            except ValueError as ex:
                return Response({'success':'false',
                                            'error_msg':"Please enter integer value for id",
                                            'errors':{},
                                            'response':{}
                                            },status=status.HTTP_400_BAD_REQUEST)

class Artist_album_data(APIView):
  
    @is_authenticate()    
    def post(self, request,pk):
        try:
            id=pk
            artist=admin_models.artist.objects.get(pk=id)
            
            
            f2=serializers.Create_artist_album(data=request.data)
            if f2.is_valid():
                album=admin_models.album()
                album.name=request.data['name']
                album.year=request.data['year']
                album.save()
                album.artist.add(artist)
                album.save()            
            
                return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK)
            return Response({'success':'false',
                                    'error_msg':'invalid_input',
                                    'errors':{},
                                    'response':{**dict(f2.errors)}
                                    },status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            return Response({'success':'false',
                                'error_msg':"please enter integer value for id",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)

# Add existing song to an artist
class Artist_song_data(APIView):
    @is_authenticate()    
    def put(self, request):
        try:
            song=admin_models.songs.objects.get(pk=int(request.POST["song_id"]))
            artist=admin_models.artist.objects.get(pk=int(request.POST["artist_id"]))
           

            
            song.artist.add(artist)
            song.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK)
        
        except  Exception as ex:
            return Response({'success':'false',
                                'error_msg':"artist or song does not exists",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)

# Remove existing song from an artist
class Artist_remove_song(APIView):
    @is_authenticate()
    def put(self,request):
        try:
            song=admin_models.songs.objects.get(pk=int(request.POST["song_id"]))
            artist=admin_models.artist.objects.get(pk=int(request.POST["artist_id"]))
            
            song.artist.remove(artist.id)
            song.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'success':'false',
                                'error_msg':"artist or song does not exists",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)

# Search Song in an Artist
class Artist_song_search_list(APIView):
    @is_authenticate()
    def get(self, request,pk):
        f1=serializers.search_song_in_artist()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    @is_authenticate()
    def post(self, request,pk):
        try:
            id=pk
            artist=admin_models.artist.objects.get(pk=id)
            songs=admin_models.songs.objects.all()
            f1=serializers.search_song_in_artist(data=request.POST)
            f2=serializers.pagination(data=request.POST)
            if not(f1.is_valid() and f2.is_valid()):
                f1.is_valid()
                f2.is_valid()
            
                return Response({'success':'false',
                                    'error_msg':'invalid_input',
                                    'errors':{},
                                    'response':{**dict(f1.errors),**dict(f2.errors)},
                                    },status=status.HTTP_400_BAD_REQUEST)
            s=request.POST['search']
            search_query=Q()
            
            if('genres' in request.POST and request.POST['genres'] != ""):
                search_query.add(Q(genres=request.POST['genres']),Q.AND)
            if s!='':
                
                search_query.add(Q(album__name__icontains=s) | Q(name__icontains=s),Q.AND)
            
            
            
            result=admin_models.songs.objects.filter(search_query,artist__id=id).distinct().order_by('-id')
            
            """
            if request.POST['order_by']!=None and request.POST['order_by']!='':
                if request.POST['order_by_type']=='dec':
                    order='-'+request.POST['order_by']
                else:
                    order=request.POST['order_by']
                result=result.order_by(order)
            """
            
            paginate_result=Paginator(result, int(request.POST['result_limit']))
            p_r=paginate_result.get_page(request.POST['page'])
        
        
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{"artist_name": artist.name, 'result':serializers.song_data(p_r,many=True).data},
                                'pagination':{'count':len(list(p_r)),
                                            'previous':'true' if p_r.has_previous() else 'false',
                                            'next':'true' if p_r.has_next() else 'false',
                                            'startIndex':p_r.start_index(),
                                            'endIndex':p_r.end_index(),
                                            'totalResults':len(list(result)),
                                    },
                                },status=status.HTTP_202_ACCEPTED)
        except ValueError as ex:
            return Response({'success':'false',
                                'error_msg':"please enter integer value for id",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)


## Search song for an Album in an Artist
class Artist_album_song_search_list(APIView):
    @is_authenticate()
    def get(self, request):
        f1=serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    @is_authenticate()
    def post(self, request):        
        if "album_id" not in request.POST or not request.POST["album_id"].isnumeric():
            return Response({'success':'false',
                                'error_msg':'Invalid album id',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        if "artist_id" not in request.POST or not request.POST["artist_id"].isnumeric():
            return Response({'success':'false',
                                'error_msg':'Invalid artist id',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        
        artist=list(admin_models.artist.objects.filter(pk=request.POST["artist_id"]))
        album=list(admin_models.album.objects.filter(pk=request.POST["album_id"]))
        if (len(artist)==0 or len(album)==0):
            return Response({'success':'false',
                                'error_msg':' artist or album does not exists',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)      
        f1=serializers.search(data=request.POST)
        f2=serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            f1.is_valid()
            f2.is_valid()
         
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors),**dict(f2.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        s=request.POST['search']
        search_query=Q()
        if s!='':
          
           
            search_query.add(Q(name__icontains=s),Q.OR)
           
            
        result=admin_models.songs.objects.filter(search_query, album=album[0].id,artist=artist[0].id).distinct().order_by('-id')
        
        """
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
        """

        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
      
      
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'album_name': album[0].name, 'artist_name':artist[0].name, 'result':serializers.song_data(p_r,many=True).data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                                },
                            },status=status.HTTP_202_ACCEPTED)


        
class Artist_remove_album(APIView):
    @is_authenticate()
    def put(self,request):
        try:
            album=admin_models.album.objects.get(pk=int(request.POST["album_id"]))
           
            
            
            
            artist=admin_models.artist.objects.get(pk=int(request.POST["artist_id"]))
           
            
            artist_album=admin_models.album.objects.filter(artist=int(request.POST["artist_id"]))
            
        
            
            
            if album in artist_album:
               
                album.artist.remove(artist)
                return Response({'success':'true',
                                        'error_msg':'',
                                        'errors':{},
                                        'response':{}
                                        },status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'success':'false',
                                'error_msg':"artist or album does not exists",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)

# Album Add, Edit, Delete, View
class albumAPI(APIView):
    @is_authenticate()
    def get(self, request,pk=None):
        if(pk.isnumeric()):
            album=list(admin_models.album.objects.filter(pk=pk))
            if album==[]:
                return Response({'success':'false',
                        'error_msg':"Data not exists in database",
                        'errors':{},
                        'response':{}
                        },status=status.HTTP_400_BAD_REQUEST) 
            f1=serializers.all_album(album[0])     

            return Response({'success':'true',
                        'error_msg':'',
                        'errors':{},
                        'response':{"artist_data":f1.data}
                        },status=status.HTTP_200_OK)
            
        else:
            return Response({'success':'false',
                                'error_msg':"please enter integer value for id",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
    @is_authenticate()
    def post(self, request):
        f2=serializers.Add_album_serializer(data=request.data)
        if f2.is_valid():
            f2.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_200_OK)
        return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f2.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)
    @is_authenticate()    
    def put(self,request,pk):
        if(pk.isnumeric()):
            album=list(admin_models.album.objects.filter(pk=pk))
            if album==[]:
                return Response({'success':'false',
                                'error_msg':"Data not exists in database",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
            f1=serializers.Add_album_serializer(album[0],data=request.data)
            if f1.is_valid():
                f1.save()
                return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_200_OK)

        else:
            return Response({'success':'false',
                                'error_msg':"please enter the integer value for id",
                                'errors':{},
                                'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST)
        
        
        
    @is_authenticate()                         
    def delete(self,request,pk):

        if(pk.isnumeric()):
            album=list(admin_models.album.objects.filter(pk=pk))
            if album==[]:
                return Response({'success':'false',
                                'error_msg':"Data not exists in database",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
            song=admin_models.songs.objects.filter(album__pk=pk)
            for sg in song:
                sg.album = None
                sg.save()
            album[0].delete()

            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK)

        else:
            return Response({'success':'false',
                                'error_msg':"please enter the integer value for id",
                                'errors':{},
                                'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST)

# Dashboard api
class dash_board(APIView):
    @is_authenticate()
    def get(self,request,pk=None):
        try:   
            artist=admin_models.artist.objects.filter().order_by('-most_played')[0:50]
            alb = admin_models.album.objects.all()
            a=alb.count()
            a_r_t = admin_models.artist.objects.all()
            ar=a_r_t.count()
            song = admin_models.songs.objects.all()
            s=song.count()
            u_s_e_r = account_models.Users.objects.all()
            u=u_s_e_r.count()
            serializer = serializers.Artist_data(artist,many =True)
            return Response({'success':'true',
                                        'error_msg':'',
                                        'errors':{''},
                                        'response':{'Exist_total_number_of_albums':a,
                                        'Exist_total_number_of_artist':ar,
                                        'Exist_total_number_of_songs':s,'Exist_total_number_of_users':u,
                                        'Top_most_50_played_artist':serializer.data},
                                        },status=status.HTTP_200_OK)
        except ValueError as ex:
            return Response ({'success':'false',
                                        'error_msg':'Please enter a integer value as ID',
                                        'errors':{},
                                        'response':{}
                                        },status=status.HTTP_400_BAD_REQUEST) 
# Album Search api
class album_search(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)

    @is_authenticate()                        
    def post(self,request):
        f1=serializers.search(data=request.POST)
        f2=serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            f1.is_valid()
            f2.is_valid()
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors),**dict(f2.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        s=request.POST['search']
        search_query=Q()
        if s!='':
            
            search_query.add(Q(name__icontains=s) | Q(year__icontains=s),Q.AND)
        
        
        result=admin_models.album.objects.select_related().filter(search_query).distinct().order_by('-id')
        #print('\n\n#result=',result[0].album.__dict__,result[0].album.year,'\n\n')
        """
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
        """
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        # print(p_r)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'result':serializers.Album_data(p_r,many=True).data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                                },
                            },status=status.HTTP_202_ACCEPTED)
# Add song to album and remove song from album
class song_album(APIView):
    @is_authenticate()
    def put(self,request):
        try:
            data= request.POST

            song = admin_models.songs.objects.filter(pk = int(data['song_id']))
            album = admin_models.album.objects.filter(id = int(data['album_id']))
            if(len(song) == 0):
                return Response({'success':'false',
                                         'error_msg':'Song not found ',
                                         'errors':{},
                                         'response':{}
                                        },status=status.HTTP_406_NOT_ACCEPTABLE)
            if(len(album) == 0):
                return Response({'success':'false',
                                         'error_msg':'Album not found ',
                                         'errors':{},
                                         'response':{}
                                        },status=status.HTTP_406_NOT_ACCEPTABLE)

            if(song[0].album):
                return Response({'success':'false',
                                        'error_msg':'Song is linked to another album ',
                                        'errors':{},
                                        'response':{}
                                        },status=status.HTTP_406_NOT_ACCEPTABLE)

            song[0].album = album[0]
            song[0].save()
            return Response({'Success':'true',
                                        'error_msg':'Song added successfully',
                                        'errors':{},
                                        'response':{""},
                                        },status=status.HTTP_200_OK) 
        except ValueError as ex:
            return Response ({'success':'false',
                                        'error_msg':'Please Enter a Integer Value As ID',
                                        'errors':{},
                                        'response':{}
                                        },status=status.HTTP_406_NOT_ACCEPTABLE)

    @is_authenticate()
    def delete(self,request,pk):
        try:
            id=pk
            songs  = list(admin_models.songs.objects.filter(pk=id))
            
            
            if len(songs)>0:
                songs[0].album=None
                songs[0].save()
                return Response({'success':'true',
                                        'error_msg':'',
                                        'errors':{},
                                        'response':{''},
                                        },status=status.HTTP_200_OK)

            return Response({'success':'false',
                                        'error_msg':'song does not exist',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
           return Response ({'success':'false',
                                        'error_msg':'ID IS NOT AN INTEGER',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)

"""
class albums_song_search_list(APIView):
    @is_authenticate()
    def get(self, request):
        f1=serializers.search_song()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    @is_authenticate()                         
    def post(self, request,pk):
        id=pk
        #album=admin_models.album.objects.get(pk=id)
        #songs=admin_models.songs.objects.all()
        f1=serializers.albums_songs_search(data=request.POST)
        f2=serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            f1.is_valid()
            f2.is_valid()
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors),**dict(f2.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        s=request.POST['search']
        flg=True
        search_query=Q()
        #search_query.add(Q(album=album),Q.OR)
        if s!='':
            flg=False
            search_query.add(Q(name__icontains=s),Q.OR)
            search_query.add(Q(album__name__icontains=s),Q.OR)
            search_query.add(Q(artist__name__icontains=s),Q.OR)
        if flg:
            result=admin_models.songs.objects.filter(album__id=id)
        else:
            result=admin_models.songs.objects.filter(search_query,album__id=id)
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'result':serializers.albums_Song_data(p_r,many=True).data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                                },
                            },status=status.HTTP_202_ACCEPTED)


"""
#view,edit,add,delete a subscription plan
class SubscriptionPlan_api(APIView):
    @ is_authenticate()
    def get(self, request,pk):
        try:
            plan=list(admin_models.SubscriptionPlan.objects.filter(pk=pk))
            if plan==[]:
                return Response({'success':'false',
                        'error_msg':"Data not exists in database",
                        'errors':{},
                        'response':{}
                        },status=status.HTTP_400_BAD_REQUEST) 
            f1=serializers.SubscriptionPlan_data(plan[0])
            return Response({'success':'true',
                        'error_msg':'',
                        'errors':{},
                        'response':{"plan_data":f1.data}
                        },status=status.HTTP_200_OK)
        except ValueError as ex:
            return Response({'success':'false',
                                'error_msg':"please enter integer value for id",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
    @is_authenticate()
    def post(self, request):
        f2=serializers.SubscriptionPlan_Data_Add(data=request.data)
        if f2.is_valid():
            f2.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_200_OK)
        return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f2.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)
                                
    @is_authenticate()    
    def put(self,request,pk):
        try:
            plan=list(admin_models.SubscriptionPlan.objects.filter(pk=pk))
            if plan==[]:
                return Response({'success':'false',
                                'error_msg':"Data not exists in database",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
            f1=serializers.SubscriptionPlan_data(plan[0],data=request.data)
            if f1.is_valid():
                f1.save()
                return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_200_OK)
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            return Response({'success':'false',
                                'error_msg':"please enter the integer value for id",
                                'errors':{},
                                'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST)
    @is_authenticate()                         
    def delete(self,request,pk):
        try:
            plan=list(admin_models.SubscriptionPlan.objects.filter(pk=pk))
            if plan==[]:
                return Response({'success':'false',
                            'error_msg':"Data not exixts in database",
                            'errors':{},
                            'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
            plan[0].delete()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK)
        except ValueError as ex:
            return Response({'success':'false',
                                'error_msg':"please enter the integer value for id",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
          
 #view a notification

class Notification_api(APIView):
    @ is_authenticate()
    def get(self, request,pk):
        try:
            notification=list(admin_models.Notification_admin.objects.filter(pk=pk))
            if notification==[]:
                return Response({'success':'false',
                        'error_msg':"Data not exists in database",
                        'errors':{},
                        'response':{}
                        },status=status.HTTP_400_BAD_REQUEST) 
            f1=serializers.Notification_data(notification[0])
            return Response({'success':'true',
                        'error_msg':'',
                        'errors':{},
                        'response':{"notification_data":f1.data}
                        },status=status.HTTP_200_OK)
        except ValueError as ex:
            return Response({'success':'false',
                                'error_msg':"please enter integer value for id",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)

# create new album for a particular artist
class Artist_album_data(APIView):
    @is_authenticate()    
    def post(self, request,pk):
        try:
            
            artist=admin_models.artist.objects.get(pk=pk)
            f2=serializers.Create_artist_album(data=request.data)
            if f2.is_valid():
                album=admin_models.album()
                album.name=request.data['name']
                album.year=request.data['year']
                album.save()
                album.artist.add(artist)
                album.save()            
                return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK)
            return Response({'success':'false',
                                    'error_msg':'invalid_input',
                                    'errors':{},
                                    'response':{**dict(f2.errors)}
                                    },status=status.HTTP_400_BAD_REQUEST)
        except ValueError as ex:
            return Response({'success':'false',
                                'error_msg':"please enter integer value for id",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
        
#add a song for a artist
class Artist_song_add(APIView):   

    @is_authenticate()    
    def put(self, request):
        try:
            song=admin_models.songs.objects.get(pk=int(request.POST["song_id"]))
            artist=admin_models.artist.objects.get(pk=int(request.POST["artist_id"]))
            song.artist.add(artist)
            song.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK)
        except  Exception as ex:
            return Response({'success':'false',
                                'error_msg':"artist or song does not exists",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)

"""
 #  search artist song by song'name&gener 
# search a song of a artist on the basis of song'name&gener
class Artist_song_search_list(APIView):
    @is_authenticate()
    def get(self, request):
        f1=serializers.search_song()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    @is_authenticate()
    def post(self, request,pk):
        try:
            artist=admin_models.artist.objects.get(pk=pk)
            f1=serializers.search(data=request.POST)
            f2=serializers.pagination(data=request.POST)
            if not(f1.is_valid() and f2.is_valid()):
                f1.is_valid()
                f2.is_valid()
                return Response({'success':'false',
                                    'error_msg':'invalid_input',
                                    'errors':{},
                                    'response':{**dict(f1.errors),**dict(f2.errors)},
                                    },status=status.HTTP_400_BAD_REQUEST)
            s=request.POST['search']
            flg=True
            search_query=Q()
            if request.POST['genres']!='':
                flg=False
                search_query.add(Q(genres=request.POST['genres']),Q.AND)
            if s!='':
                flg=False
                search_query.add(Q(name__icontains=s),Q.OR)
                search_query.add(Q(genres__icontains=s),Q.OR)
            if flg:
                result=admin_models.songs.objects.filter(artist__id=id)
            else:
                result=admin_models.songs.objects.filter(search_query,artist__id=id)
            if request.POST['order_by']!=None and request.POST['order_by']!='':
                if request.POST['order_by_type']=='dec':
                    order='-'+request.POST['order_by']
                else:
                    order=request.POST['order_by']
                result=result.order_by(order)
            paginate_result=Paginator(result, int(request.POST['result_limit']))
            p_r=paginate_result.get_page(request.POST['page'])
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{'result':serializers.Artist_song_data(p_r,many=True).data},
                                'pagination':{'count':len(list(p_r)),
                                            'previous':'true' if p_r.has_previous() else 'false',
                                            'next':'true' if p_r.has_next() else 'false',
                                            'startIndex':p_r.start_index(),
                                            'endIndex':p_r.end_index(),
                                            'totalResults':len(list(result)),
                                    },
                                },status=status.HTTP_202_ACCEPTED)
        except Exception as ex:
            return Response({'success':'false',
                                'error_msg':"please enter integer value for id or artist not exists ",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)

#search of song inside a album of a artist on basis of song's name
class Artist_album_song_search_list(APIView):
"""         


# Search Songs in an album
class albums_song_search_list(APIView):
    @is_authenticate()
    def get(self, request):
        f1=serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    @is_authenticate()                         
    def post(self, request,pk):
        id=pk
        #album=admin_models.album.objects.get(pk=id)
        #songs=admin_models.songs.objects.all()
        f1=serializers.search(data=request.POST)
        f2=serializers.pagination(data=request.POST)
        album = list(admin_models.album.objects.filter(id=id))
        if(album == []):
            return Response({'success':'false',
                                'error_msg':'Album not found',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        if not(f1.is_valid() and f2.is_valid()):
            f1.is_valid()
            f2.is_valid()
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors),**dict(f2.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        
        s=request.POST['search']
        search_query=Q()
        search_query.add(Q(album__id=id),Q.AND)
        if s!='':
            search_query.add(Q(name__icontains=s) | Q(album__name__icontains=s) | Q(artist__name__icontains=s),Q.AND)
        
        result=admin_models.songs.objects.filter(search_query).distinct().order_by('-id')
        
        
        """
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
        """
        
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'album_name': album[0].name, 'result':serializers.song_data(p_r,many=True).data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                                },
                            },status=status.HTTP_202_ACCEPTED)

#remove a song from a artist
class Artist_remove_song(APIView):
    @is_authenticate()
    def put(self,request):
        try:
            song=admin_models.songs.objects.get(pk=int(request.POST["song_id"]))
            artist=admin_models.artist.objects.get(pk=int(request.POST["artist_id"]))
            artist_songs=admin_models.songs.objects.filter(artist=int(request.POST["artist_id"]))
            if song in artist_songs:
                song.artist.remove(artist)
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{}
                                    },status=status.HTTP_200_OK)
            return Response({'success':'false',
                                    'error_msg':'song is not linked with artist',
                                    'errors':{},
                                    'response':{}
                                    },status=status.HTTP_200_OK)
        except Exception as ex:
            return Response({'success':'false',
                                'error_msg':"artist or song does not exists",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
    
                                
#to create a new  playlist by user
class Create_User_Playlist_For_Admin(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.User_Playlist_By_Admin()
        return Response({**f1.data,
                            },status=status.HTTP_200_OK)
    @is_authenticate()
    def post(self,request):
        f1=serializers.User_Playlist_By_Admin(data=request.data)
        if f1.is_valid():
            f1.save()
            return Response({'success':'true',
                              'error_msg':'',
                              'errors':{},
                              'response':{}
                              },status=status.HTTP_200_OK)
        return Response({'success':'false',
                                'error_msg':"",
                                'errors':{},
                                'response':{**dict(f1.errors)}
                                },status=status.HTTP_400_BAD_REQUEST)
#liked song by user
class User_Liked_Songs_By_Admin(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    
    @is_authenticate()
    def post(self, request,pk):
        f1=serializers.search(data=request.POST)
        f2=serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            return Response({'success':'false',
                            'error_msg':'invalid_input',
                            'errors':{},
                            'response':{**dict(f1.errors),**dict(f2.errors)},
                            },status=status.HTTP_400_BAD_REQUEST)
        search=request.data["search"] 
        if search!="":
            result=list(admin_models.songs.objects.filter((Q(likes=pk)&(Q(name__icontains=search)|Q(artist__name__icontains=search)|Q(album__name__icontains=search)))).distinct())
        else:   
             result=list(admin_models.songs.objects.filter(likes=pk))
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
                result=result.order_by(order)
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        f1=serializers.User_Liked_Songs_By_Admin(result,many=True)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'result':f1.data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                            },   
                            },status=status.HTTP_202_ACCEPTED)

"""
class User_Liked_Songs_By_Admin(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.search()
        return Response(f1.data,status=status.HTTP_200_OK)
    @is_authenticate()
    def post(self, request,pk):
        try:
            search=request.data["search"]
            if int(pk)>int(len(account_models.Users.objects.all())):
                return Response({'success':'false',
                            'error_msg':"user not exists",
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_400_BAD_REQUEST)
            elif search!="":
                result=list(admin_models.songs.objects.filter(likes=pk,name__icontains=search))
                f1=serializers.User_Liked_Songs_By_Admin(result,many=True)
                print("len",len(account_models.Users.objects.all()))
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':f1.data,
                                    },status=status.HTTP_200_OK)
            result=list(admin_models.songs.objects.filter(likes=pk))
            f1=serializers.User_Liked_Songs_By_Admin(result,many=True)
            return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':f1.data,
                                    },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success':'false',
                                'error_msg':"Enter a integer value for id",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)
"""
#subscription plan history of user                             
class User_Subscription_Plan_History_For_Admin(APIView):
    @is_authenticate()
    def get(self, request,pk):
        try:
            data=list(admin_models.Subscription_History.objects.filter(user=pk))
            print("test",data)
            f1=serializers.Admin_User_Subscription_Plan(data,many=True)
           
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{"data":f1.data}
                                },status=status.HTTP_200_OK) 
        except Exception as e:
            return Response({'success':'false',
                    'error_msg':'id is not valid or data not exist',
                    'errors':{},
                    'response':{}
                    },status=status.HTTP_400_BAD_REQUEST)

class Artist_Album_Remove_Song(APIView):
    def put(self,request):
        try:
            artist=admin_models.artist.objects.get(pk=request.data["artist_id"])
            print(artist)

            album=admin_models.album.objects.get(pk=request.data["album_id"])
            print(album)
            song=admin_models.songs.objects.get(pk=request.data["song_id"])
            album_of_artist=admin_models.album.objects.filter(artist=request.data["artist_id"])
            print(album_of_artist)
            if album not in album_of_artist:
                return Response({'success':'false',
                                    'error_msg':"artist is not linked to album",
                                    'errors':{},
                                    'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST)
            songs_of_album=admin_models.songs.objects.filter(album=request.data["album_id"])
            songs_of_artist=admin_models.songs.objects.filter(artist=request.data["artist_id"])
            if song not in songs_of_album and song not in songs_of_artist:
                return Response({'success':'false',
                                    'error_msg':"song not exists in artist or album",
                                    'errors':{},
                                    'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST)
            if album in album_of_artist and song in songs_of_artist and song in songs_of_album:
                song.album=None
                song.save()
                return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_200_OK) 
            return Response({'success':'false',
                                    'error_msg':"song not exists in artist or album",
                                    'errors':{},
                                    'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return Response({'success':'false',
                                    'error_msg':"song or artist or album not exists ",
                                    'errors':{},
                                    'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST)

#to get the active subscription plan of user                           
class User_Current_Subscription_Plan(APIView):
    @is_authenticate()
    def get(self,request,pk):
        try:
            data=admin_models.Subscription_History.objects.filter(user=pk).latest("expire")
            f1=serializers.Admin_User_Subscription_Plan(data)
            if data.expire>timezone.now():
                return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{"data":f1.data}
                            },status=status.HTTP_200_OK) 
            return Response({'success':'false',
                        'error_msg':'no active plan',
                        'errors':{},
                        'response':{}
                        },status=status.HTTP_400_BAD_REQUEST) 
        except Exception as ex:
            return Response({'success':'false',
                    'error_msg':'id is not valid or data not exist',
                    'errors':{},
                    'response':{}
                    },status=status.HTTP_400_BAD_REQUEST)


class User_Feedback(APIView):      
    def get(self,request,pk):
        if(pk.isnumeric()):
            feedback=list(admin_models.Feedback.objects.filter(pk=pk))   
            f1=serializers.Users_feedback(feedback,many=True)
            if feedback==[]:
                return Response({'success':'false',
                                    'error_msg':'Data does not Exist',
                                    'errors':{},
                                    'response':{}
                                    },status=status.HTTP_200_OK) 
            return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{"Feedback data":f1.data}
                                    },status=status.HTTP_200_OK)   
        else:
            return Response({'success':'false',
                                'error_msg':"please enter integer value for id",
                                'errors':{},
                                'response':{}
                                },status=status.HTTP_400_BAD_REQUEST)




        
            

       
       

        



 

                            



          




   

   
       

                
