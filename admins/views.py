from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework import status
from django.db.models import Q, manager
from admins import models as admin_models
from accounts import models as account_models
from .models import playlist_admin, songs
# Create your views here.
import bcrypt
from accounts import tools
import datetime
from . import serializers
from .serializers import playlist_admin_form,song_data
from django.http import Http404
# from . import tools
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
            if name in []:
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
        f1=serializers.admin_data(requstuser)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':f1.data,
                            },status=status.HTTP_200_OK)
    @is_authenticate()
    def post(self,request):
        
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        f1=serializers.admin_form(instance=requstuser,data=request.POST)
        f1.is_valid()
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)},
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
            hash_pass=requstuser.password.encode('utf-8')

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
            search_query.add(Q(first_name__icontains=s),Q.OR)
            search_query.add(Q(last_name__icontains=s),Q.OR)
            search_query.add(Q(phone_number__icontains=s),Q.OR)
            search_query.add(Q(country__icontains=s),Q.OR)
            search_query.add(Q(state__icontains=s),Q.OR)
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
                            'response':{'result':serializers.search_consumer_form(p_r,many=True).data},
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
    def post(self,request,id):
        user=list(account_models.Users.objects.filter(id=id))
        if user==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        user=user[0]
        f1=serializers.search_consumer_form(instance=user,data=request.POST)
        f1.is_valid()
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
    def get(self,request,id):
        user=list(account_models.Users.objects.filter(id=id))
        if user==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        user=user[0]
        try:
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
    def get(self,request):
        f1=serializers.pagination(data=request.POST)
        if not(f1.is_valid() ):
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        result=list(account_models.Admins.objects.filter(~Q(id=requstuser.id)))
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
        if user==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        user=user[0]
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
            if requstuser.profile_pic != 'deafult_profile_pic.jpeg':
                requstuser.profile_pic.delete()
            uzr.profile_pic=request.FILES['profile_pic']
        uzr.save()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},

                            },status=status.HTTP_200_OK)
class delete_subadmin(APIView):
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
        try:
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
class song_search_list(APIView):
    def get(self,request):
        f1=serializers.search_song()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    def post(self,request):
        f1=serializers.search_song(data=request.POST)
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
            search_query.add(Q(name__icontains=s),Q.OR)
            search_query.add(Q(album__name__icontains=s),Q.OR)
            search_query.add(Q(artist__name__icontains=s),Q.OR)
            search_query.add(Q(artist__name__icontains=s),Q.OR)
            search_query.add(Q(charts__icontains=s),Q.OR)
        if flg:
            result=admin_models.songs.objects.select_related()
        else:
            result=admin_models.songs.objects.select_related().filter(search_query)
        print('\n\n#result=',result[0].album.__dict__,result[0].album.year,'\n\n')
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
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
#searching for specific playlist
class get_playlist_admin(APIView):
    def get(self,request):
        f1=serializers.search_song()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    def post(self,request):
        f1=serializers.search_song(data=request.POST)
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
            search_query.add(Q(name__icontains=s),Q.OR)
            search_query.add(Q(gener__icontains=s),Q.OR)
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
            
            
        f1=playlist_admin_form(snippet[0])
        print(f1.data)
        snippet[0].delete()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{"deleted":{**dict(f1.data)}},
                            },status=status.HTTP_200_OK)
    
class playlist_admin_get(APIView): 
    @is_authenticate()
    def get(self,request):
        temp=admin_models.playlist_admin.objects.all()
        f1=playlist_admin_form(temp,many=True)
        return Response(f1.data
                            ,status=status.HTTP_202_ACCEPTED)


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
    




                        



'''


def error_404_view(request, exception):
    a={"status":"page not found"}
    return render(request,'404.html',a)
'''            
            
            #success only boolean