from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework import status
from django.db.models import Q
from admins import models as admin_models
from accounts import models as account_models
# Create your views here.
import bcrypt
from accounts import tools
import datetime
from . import serializers
import random
import secrets
from accounts.views import login_admin
from admins import serializers as admin_serializers
from accounts import models as account_models
# from . import tools
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
class recomended_playlist(APIView):
    @is_authenticate()
    def get(self,request):
        gener=['pop','dance&electronics','rock','rockstar','bollywood','folk&acoustic']
        gener=random.choice(gener)
        playlist=list(admin_models.playlist_admin.objects.prefetch_related().filter(gener__icontains=gener))
        if playlist==[]:
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{},#"songs":serializers.song_data(playlist.songs.all(),many=True).data
                                },status=status.HTTP_200_OK)
        if len(playlist)<2:
            playlist=playlist[0]
        else:
            playlist=playlist[random.randint(0,len(playlist))]
        f1=serializers.playlist_admin_data(playlist)

        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{"playlist_data":f1.data},#"songs":serializers.song_data(playlist.songs.all(),many=True).data
                            },status=status.HTTP_200_OK)

#edit the profile of a user
class Edit_User_Profile(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.Edit_User_Profile()
        return Response(f1.data,status=status.HTTP_200_OK)

    @is_authenticate()
    def post(self,request):
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        print("test",data)
        requstuser=tools.get_user(*data)
        f1=serializers.Edit_User_Profile(instance=requstuser,data=request.data)
        if not(f1.is_valid()):
            return Response({'success':'false',
                                'error_msg':'invalid_input',
                                'errors':{},
                                'response':{**dict(f1.errors)},
                                },status=status.HTTP_400_BAD_REQUEST)
        f1.save()
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK)

#change user password in case he remembers his password but nedd to change it
class Change_User_Password(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.change_password()
        return Response(f1.data,status=status.HTTP_200_OK)
        
    @is_authenticate()
    def post(self,request):
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        f1=serializers.change_password(instance=requstuser,data=request.POST)
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
#to create a playlist for user
class Create_Playlist(APIView):
    @is_authenticate()
    def get(self, request): 
        f1=serializers.Create_Playlist()
        return Response(f1.data,status=status.HTTP_200_OK)

    @is_authenticate()
    def post(self, request):
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        f1=serializers.Create_Playlist(data=request.POST)
        if f1.is_valid():
            p=f1.save()
            p.user=requstuser
            p.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
        return Response({'success':'false',
                                'error_msg':'',
                                'errors':{**dict(f1.errors)},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
#to add a song in a playlist of an artist
class Add_Song_Playlist(APIView):
    @is_authenticate()
    def post(self,request):
        try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            song=admin_models.songs.objects.get(pk=request.data["song_id"])
            playlist=admin_models.playlist_admin.objects.get(pk=request.data["playlist_id"])
            if playlist.user==requstuser:
                playlist.songs.add(song)
                playlist.save()
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_200_OK)
            return Response({'success':'false',
                                    'error_msg':'"user dont have this playlist',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return  Response({'success':'false',
                                'error_msg':'invalid input',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

# to see all the albums of an artist
class Aritst_All_Albums_List(APIView):
    @is_authenticate()
    def get(self, request,pk):
        try:
            artist=admin_models.artist.objects.get(pk=pk)
            album=list(admin_models.album.objects.filter(songs__artist__pk=pk).order_by("-year").distinct())
            if album!=[]:
                f1=admin_serializers.Artist_Album_Data(album,many=True)
                f2=serializers.Artist_Data(artist)
                return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{"artist":f2.data,"albums":f1.data}
                                },status=status.HTTP_200_OK)
            return  Response({'success':'false',
                                'error_msg':' album not exists',
                                'errors':{},
                                'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success':'false',
                                'error_msg':'invalid input',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
                               
# to see all the albums of an artist
class Aritst_All_Playlist_List(APIView):
    def get(self, request,pk):
        try:
            #data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            #requstuser=tools.get_user(*data)
            #if user==requstuser:
            playlist=list(admin_models.playlist_admin.objects.filter(songs__artist__pk=pk).order_by("-year").distinct())
            artist=admin_models.artist.objects.get(pk=pk)
            if playlist!=[]:
                f1=serializers.Artist_Playlist_List(playlist,many=True)
                f2=serializers.Artist_Data(artist)
                return Response({'success':'true',
                                            'error_msg':'',
                                            'errors':{},
                                            'response':{"artist":f2.data,"playlist":f1.data},
                                            },status=status.HTTP_200_OK)
            return  Response({'success':'false',
                                'error_msg':' playlist not exists',
                                'errors':{},
                                'response':{},
                                 },status=status.HTTP_400_BAD_REQUEST)
    
        except Exception as e:
            return Response({'success':'false',
                                'error_msg':'invalid input',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
                                

#to see all the songs of an artist
class Artist_Song_List(APIView):
 def get(self, request,pk):
        try:
            song=list(admin_models.songs.objects.filter(artist__pk=pk).order_by("-year").distinct())
            artist=admin_models.artist.objects.get(pk=pk)
            if song!=[]:
                f1=admin_serializers.Song_data(song,many=True)
                f2=serializers.Artist_Data(artist)
                return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{"artist":f2.data,"song":f1.data},
                                },status=status.HTTP_200_OK)
            return  Response({'success':'false',
                                'error_msg':' song not exists',
                                'errors':{},
                                'response':{},
                                 },status=status.HTTP_400_BAD_REQUEST)
    
        except Exception as e:
            return Response({'success':'false',
                                'error_msg':'invalid input',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
                      
 
                                
          
          










        
   
 
   

   

                          
   




    
    
