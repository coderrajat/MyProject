from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from admins import models as admin_models
# Create your views here.
import bcrypt
from accounts import tools
from . import serializers
# from . import tools
def is_authenticate(*Dargs,**Dkwargs):
    def inner(func):
        def wrapper(*args,**kwargs):

            if 'HTTP_AUTHORIZATION'in args[1].META :
                try:
                    data=tools.decodetoken(args[1].META['HTTP_AUTHORIZATION'])

                    time=datetime.datetime.strptime(data[2].split('.')[0],'%Y-%m-%d %H:%M:%S')
                except:
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
    def get(self,request,name):
        content=list(admin_models.CMS.objects.filter(name=name))
        if content==[]:
            if name in []:
                cms=admin_models.CMS()
                cms.name=name
                cms.save()
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{'data':serializers.csm_about_us_api(cms).data},
                                    },status=status.HTTP_202_ACCEPTED)
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
                            },status=status.HTTP_202_ACCEPTED)
    def post(self,request,name):
        f1=serializers.csm_about_us_api(data=request.POST,instance=content)
        if f1.is_valid():
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
                                        'response':{'data':serialize('json', [cms])},
                                        },status=status.HTTP_202_ACCEPTED)
                else:
                    return Response({'success':'false',
                                        'error_msg':name+' is a invalid term or policy',
                                        'errors':{},
                                        'response':{},
                                        },status=status.HTTP_400_BAD_REQUEST)
            content=content[0]
            content.content=request.POST['content']
            content.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{'data':serialize('json', [content])},
                                },status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'success':'false',
                                'error_msg':'CMS_content not valid',
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

class image_settings(APIView):


    # @is_authenticate(
    # change_company_details =True,
    # )
    def get(self,request):
        ims=admin_models.image_settings.objects.get_or_create(id='1',defaults={'deafult_profile_pic': 'deafult_profile_pic.jpeg','default_parking_spot_pic': 'default_parking_spot_pic.jpeg'})[0]
        f1=serializers.image_settings(ims)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'result':f1.data},
                            },status=status.HTTP_202_ACCEPTED)



    # @is_authenticate(
    # change_company_details =True,
    # )
    def post(self,request):

        ims=admin_models.image_settings.objects.get_or_create(id='1',defaults={'deafult_profile_pic': 'deafult_profile_pic.jpeg','default_parking_spot_pic': 'default_parking_spot_pic.jpeg'})[0]
        f1=serializers.image_settings_base64(data=request.POST)

        for i in request.POST.keys():

            if ';base64,'in request.POST[i]:
                dt=get_base64_to_img(request.POST[i])
                getattr(ims, i).delete()
                getattr(ims, i).save(i+'.jpeg',dt[0],save=True)

        return Response({'success':'true',
                    'error_msg':'in',
                    'errors':{},
                    'response':{},
                    },status=status.HTTP_202_ACCEPTED)

class smtp_settings_api(APIView):
    # @is_authenticate(
    # change_company_details =True,
    # )
    def get(self,request):
        f1=serializers.smtp_settings_api(list(admin_models.SMTP_setting.objects.filter(id=1))[0])
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{**f1.data},
                            },status=status.HTTP_202_ACCEPTED)


    # @is_authenticate(
    # change_company_details =True,
    # )
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
                                    },status=status.HTTP_202_ACCEPTED)
            else:
                return Response({'success':'false',
                                    'error_msg':beautify_errors({**dict(f1.errors)}),
                                    'errors':{**dict(f1.errors)},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
class social_media_settings(APIView):


    # @is_authenticate(
    # change_company_details =True,
    # )
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
                            },status=status.HTTP_202_ACCEPTED)

    # @is_authenticate(
    # change_company_details =True,
    # )
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
                                },status=status.HTTP_202_ACCEPTED)
        else:
            return Response({'success':'false',
                                    'error_msg':beautify_errors({**dict(f1.errors)}),
                                    'errors':{**dict(f1.errors)},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)

class general_settings_api(APIView):
    # @is_authenticate()
    def get(self, request):
        g_s = admin_models.general_settings.objects.get(id = 1)
        return Response({'data':serializers.general_settings_serializer(g_s).data,
                            },status=status.HTTP_202_ACCEPTED)
    # @is_authenticate(change_company_details =True,)
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
                                },status=status.HTTP_202_ACCEPTED)

        else:
            f1.is_valid()
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
