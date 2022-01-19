from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework import status
from django.db.models import Q
from django.utils import timezone

#from Mayani_Backend.admins.views import song_album
from admins import models as admin_models
from accounts import models as account_models
import bcrypt
from accounts import tools
import datetime
from datetime import timedelta
from . import serializers
import random
import secrets

from admins import serializers as admin_serializers
#from accounts import models as account_models
from accounts import models as account_models
import os
from django.utils import timezone
import boto3
import json

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
        print('hiiiii',gener)
        playlist=list(admin_models.playlist_admin.objects.prefetch_related().filter(gener__icontains=gener))
        print(playlist)
        if playlist==[]:
            #a=serializers.song_data(playlist.songs.all())
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{},#"songs":serializers.song_data(playlist.songs.all(),many=True).data
                                },status=status.HTTP_200_OK)
        if len(playlist)<5:
            playlist=playlist[0]
        else:
            playlist=playlist[random.randint(0,len(playlist))]
        f1=serializers.playlist_admin_data(playlist)

        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{"playlist_data":f1.data},#"songs":serializers.song_data(playlist.songs.all(),many=True).data
                            },status=status.HTTP_200_OK)

# search api search by song name ,artist name, album name, gneres name
class Songs_search(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.search_song()
        f2=serializers.pagination()
        print(f1.data)
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    @is_authenticate()                          
    def post(self,request):
        f1=serializers.search_song(data=request.POST)
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
        #print(flg)
        if s!='':
            flg=False
            search_query=Q()  
            search_query.add(Q(name__icontains=s) | Q(album__name__icontains=s) | Q(artist__name__icontains=s) | Q(genres__icontains=s),Q.AND)
            #search_query.add(Q(charts__icontains=s),Q.OR)
        if flg:
            result=admin_models.songs.objects.select_related().order_by('-id')
        else:
            result=admin_models.songs.objects.filter(search_query).distinct().order_by('-id')
        #print('\n\n#result=',result[0].album.__dict__,result[0].album.year,'\n\n')
        '''
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
            '''
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        
        p_r=paginate_result.get_page(request.POST['page'])

        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{'result':admin_serializers.song_data(p_r,many=True).data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                                },
                            },status=status.HTTP_202_ACCEPTED)

'''
#get all song from particuler album
class Albums_songs(APIView):
    @is_authenticate()
    def get(self, request,pk):
        try:
            album=admin_models.album.objects.get(pk=pk)
            song_album=list(admin_models.album.objects.filter(songs__album__pk=pk))

            a=serializers.Album_songs(song_album,many=True)
            return  Response({'success':'True',
                                'error_msg':'',
                                'errors':{},
                                'response':{'Albums':album.name,'Album,s Songs':a.data},
                                    },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success':'false',
                                'error_msg':'invalid input',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST) 

'''
#get song with the help of search limit from particuler album

class Albums_songs(APIView):
    @is_authenticate()
    def post(self, request,pk):
        try:
            album=admin_models.album.objects.get(pk=pk)
            result=admin_models.songs.objects.filter(album__id=pk).distinct().order_by('-id')
            paginate_result=Paginator(result, int(request.POST['result_limit']))
            p_r=paginate_result.get_page(request.POST['page'])
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{"album_name": album.name, 'result':admin_serializers.song_data(p_r,many=True).data},
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


#edit the profile of a user
class Edit_User_Profile(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.Edit_User_Profile()
        return Response(f1.data,status=status.HTTP_200_OK)

    @is_authenticate()
    def post(self,request):
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        user=list(account_models.Users.objects.filter(Q(phone_number=request.data["phone_number"]) & Q(country_code=request.data["country_code"])&~ Q(id=requstuser.id)))
        if user!=[] :
                return Response({'success':'false',
                            'error_msg':'mobile number already exists',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST)
        user=requstuser
        f1=serializers.Edit_User_Profile(user,data=request.data)     
        if not(f1.is_valid()):
            return Response({'success':'false',
                            'error_msg':'',
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
        f1=serializers.change_password(requstuser,data=request.POST)
        if f1.is_valid():
            if request.POST['password']=='':
                return Response({'success':'false',
                                'error_msg':'Passwords should not empty',
                                'errors':{},
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
                                    'error_msg':'Confirm Password does not match',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'success':'false',
                                'error_msg':'Old Password is incorrect',
                                'errors':{},
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
            song=list(admin_models.songs.objects.filter(pk=request.data["song_id"]))
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
                            'error_msg':'playlist_id & song_id are required',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST)


# to see all the albums of an artist

class Aritst_All_Albums_List(APIView):
    @is_authenticate()
    def get(self,request):
        f1=admin_serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    
    @is_authenticate()
    def post(self, request):
        artist_id=request.data["artist_id"]
        f1=admin_serializers.search(data=request.POST)
        f2=admin_serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            return Response({'success':'false',
                            'error_msg':'invalid_input',
                            'errors':{},
                            'response':{**dict(f1.errors),**dict(f2.errors)},
                            },status=status.HTTP_400_BAD_REQUEST)
        search=request.data["search"] 
        if search!="":
            
        
            result=list(admin_models.album.objects.filter((Q(songs__artist__pk=artist_id)&(Q(name__icontains=search)|Q(year__icontains=search)))).order_by("year").distinct())
        else:   
            result=list(admin_models.album.objects.filter(songs__artist__pk=artist_id).order_by("-year").distinct())
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
                result=result.order_by(order)
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        f1=admin_serializers.User_Liked_Songs_By_Admin(result,many=True)
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
                            },status=status.HTTP_202)

class Aritst_All_Playlist_List(APIView):
    @is_authenticate()
    def get(self,request):
        f1=admin_serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    
    @is_authenticate()
    def post(self, request):
        artist_id=request.data["artist_id"]
        f1=admin_serializers.search(data=request.POST)
        f2=admin_serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            return Response({'success':'false',
                            'error_msg':'invalid_input',
                            'errors':{},
                            'response':{**dict(f1.errors),**dict(f2.errors)},
                            },status=status.HTTP_400_BAD_REQUEST)
        search=request.data["search"] 
        if search!="":
            
        
            result=list(admin_models.playlist_admin.objects.filter((Q(songs__artist__pk=artist_id)&(Q(name__icontains=search)|Q(year__icontains=search)|Q(song__icontains=search)))).order_by("year").distinct())
        else:   
            result=list(admin_models.playlist_admin.objects.filter(songs__artist__pk=artist_id).order_by("-year").distinct())
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
                result=result.order_by(order)
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        f1=admin_serializers.User_Liked_Songs_By_Admin(result,many=True)
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
# to see all the albums of an artist
class Aritst_All_Playlist_List(APIView):
    @is_authenticate()
    def get(self, request,pk):
        try:
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
                            """
                                
#to see all the songs of an artist
class Artist_All_Song_List(APIView):
    @is_authenticate()
    def get(self,request):
        f1=admin_serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    
    @is_authenticate()
    def post(self, request):
        artist_id=request.data["artist_id"]
        f1=admin_serializers.search(data=request.POST)
        f2=admin_serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            return Response({'success':'false',
                            'error_msg':'invalid_input',
                            'errors':{},
                            'response':{**dict(f1.errors),**dict(f2.errors)},
                            },status=status.HTTP_400_BAD_REQUEST)
        search=request.data["search"] 
        if search!="":
            
        
            result=list(admin_models.songs.objects.filter((Q(artist__pk=artist_id)&(Q(name__icontains=search)|Q(year__icontains=search)))).order_by("year").distinct())
        else:   
            result=list(admin_models.songs.objects.filter(artist__pk=artist_id).order_by("-year").distinct())
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
                result=result.order_by(order)
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        f1=serializers.Song_Data(result,many=True)
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
class Artist_All_Song_List(APIView):
 @is_authenticate()
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
                      
 
        
          """



#all liked songs of a user
class User_Liked_Songs(APIView):
    @is_authenticate()
    def get(self,request):
        f1=admin_serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    
    @is_authenticate()
    def post(self, request):
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        f1=admin_serializers.search(data=request.POST)
        f2=admin_serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            return Response({'success':'false',
                            'error_msg':'invalid_input',
                            'errors':{},
                            'response':{**dict(f1.errors),**dict(f2.errors)},
                            },status=status.HTTP_400_BAD_REQUEST)
        search=request.data["search"] 
        if search!="":
            result=list(admin_models.songs.objects.filter((Q(likes=requstuser.id)&(Q(name__icontains=search)|Q(artist__name__icontains=search)|Q(album__name__icontains=search)))).distinct())
        else:   
             result=list(admin_models.songs.objects.filter(likes=requstuser.id))
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
                result=result.order_by(order)
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        f1=admin_serializers.User_Liked_Songs_By_Admin(result,many=True)
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



#all downloaed songs of a user
class User_Downloaded_Songs(APIView):
    def get(self,request):
        f1=admin_serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    @is_authenticate()
    def post(self, request):
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        f1=admin_serializers.search(data=request.POST)
        f2=admin_serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            return Response({'success':'false',
                            'error_msg':'invalid_input',
                            'errors':{},
                            'response':{**dict(f1.errors),**dict(f2.errors)},
                            },status=status.HTTP_400_BAD_REQUEST)
        search=request.data["search"] 
        if search!="":
            result=list(admin_models.songs.objects.filter((Q(downloads=requstuser.id)&(Q(name__icontains=search)|Q(artist__name__icontains=search)|Q(album__name__icontains=search)))).distinct())
        else:   
             result=list(admin_models.songs.objects.filter(downloads=requstuser.id))
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
                result=result.order_by(order)
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        f1=admin_serializers.User_Liked_Songs_By_Admin(result,many=True)
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
        


#all playlist created by a user    
class User_Playlist(APIView):
    @is_authenticate()
    def get(self,request):
        f1=serializers.search()
        return Response(f1.data,status=status.HTTP_200_OK)
    
    @is_authenticate()
    def post(self, request):
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        f1=admin_serializers.search(data=request.POST)
        f2=admin_serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            return Response({'success':'false',
                            'error_msg':'invalid_input',
                            'errors':{},
                            'response':{**dict(f1.errors),**dict(f2.errors)},
                            },status=status.HTTP_400_BAD_REQUEST)
        search=request.data["search"] 
        if search!="":
            result=list(admin_models.playlist_admin.objects.filter((Q(user__id=requstuser.id)&(Q(name__icontains=search)|Q(gener__icontains=search)))).distinct())
        else:   
             result=list(admin_models.playlist_admin.objects.filter(user__id=requstuser.id))
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
            result=result.order_by(order)
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        f1=admin_serializers.playlist_admin_data(result,many=True)
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


#to like a song by user
class Like_Song_By_User(APIView):
    @is_authenticate()
    def get(self,request,song_id):
        try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            song=admin_models.songs.objects.get(pk=song_id)
            song.likes.add(requstuser.id)
            song.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK) 
        except Exception as e:
            return  Response({'success':'false',
                            'error_msg':'invalid id',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST)



#to dislike a song by user
class Dislike_Song_By_User(APIView):
    @is_authenticate()
    def get(self,request,song_id):
        try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            song=admin_models.songs.objects.get(pk=song_id)
            song.likes.remove(requstuser.id)
            song.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'success':'false',
                            'error_msg':'invalid id',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST)


#to like a album by user
class  Like_Album_By_User(APIView):
    @is_authenticate()
    def get(self,request,album_id):
        try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            album=admin_models.album.objects.get(pk=album_id)
            album.likes.add(requstuser.id)
            album.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK) 
        except Exception as e:
            return  Response({'success':'false',
                            'error_msg':'invalid id',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST)

#remove songs from the specific playlist
class Remove_Song_Playlist(APIView):
    @is_authenticate()
    def post(self,request):
        try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            song=admin_models.songs.objects.get(pk=request.data["song_id"])
            play_list=admin_models.playlist_admin.objects.get(pk=request.data["playlist_id"])
            if play_list.user==requstuser:
                play_list.songs.remove(song)
                play_list.save()
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_200_OK)
            return Response({'success':'false',
                                    'error_msg':'User does not Exist in this playlist',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return  Response({'success':'false',
                                'error_msg':'invalid input',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

#delete playlist api 
class User_delete_playlist(APIView):
    @is_authenticate()
    def post(self,request):
        try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            play_list=admin_models.playlist_admin.objects.get(pk=request.data["playlist_id"])
            if play_list.user==requstuser:
                play_list.songs.remove()
                play_list.delete()
                return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_200_OK)
            return Response({'success':'false',
                                    'error_msg':'User does not Exist in this playlist',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            return  Response({'success':'false',
                                'error_msg':'invalid input',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

class recomended_artist(APIView):
    @is_authenticate()
    def get(self,request,id):
        art=random.choice(id)
        artist=list(admin_models.artist.objects.filter(songs__artist__id=art))
        #print(artist)
        if artist==[]:
            return Response({'success':'false',
                                'error_msg':'',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
        if len(artist)<2:
            artist=artist[0]
        else:
            artist=artist[random.randint(0,len(artist))]
        f1=serializers.artist_songs(artist)

        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{"Artist_data":f1.data},
                            },status=status.HTTP_200_OK)
#show CMS content
class Cms(APIView):
    @is_authenticate()
    def get(self,request,name):
        content=list(admin_models.CMS.objects.filter(name=name))
        if content==[]:
            if name in ['about_us','legal_disclamer','t&c','privacy_policy']:
                cms=admin_models.CMS()
                cms.name=name
                cms.save()   
                '''  
                return Response({'success':'true',
                                            'error_msg':'',
                                            'errors':{},
                                            'response':{'dataaaaa':admin_serializers.csm_about_us_api(cms).data},
                                            },status=status.HTTP_200_OK)  
                '''                                       
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
                        'response':{'data':admin_serializers.csm_about_us_api(content).data},
                        },status=status.HTTP_200_OK)
#showing FAQ
class Faq_section(APIView):
    @ is_authenticate()
    def get(self,request,pk=None):
        try:
            if pk is not None:
                fq=list(admin_models.faq.objects.filter(pk=pk))
                '''
                if fq==[]:
                    return Response({'success':'false',
                                     'error_msg':"Data does not exist",
                                     'errors':{},
                                     'response':{}
                                    },status=status.HTTP_400_BAD_REQUEST) 
                '''
                fq2=admin_serializers.faq_category(fq[0])
                return Response({'success':'true',
                                     'error_msg':'',
                                     'errors':{},
                                     'response':{"FAQ_data":fq2.data}
                                     },status=status.HTTP_200_OK)
            fq=admin_models.faq.objects.all()
            fq2=admin_serializers.faq_category(fq,many=True)
            
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

#User will add feedback                                  
class User_Feedback(APIView):
    @is_authenticate()
    def get(self, request): 
        f1=serializers.User_feed_back()
        return Response(f1.data,status=status.HTTP_200_OK)
#to dislike a album by user
class Dislike_Album_By_User(APIView):
    def get(self,request,album_id):
        try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            album=admin_models.album.objects.get(pk=album_id)
            album.likes.remove(requstuser.id)
            album.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            return  Response({'success':'false',
                            'error_msg':'invalid id',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST)
                                

# user can follow a artist
class Artist_Follow_By_User(APIView):
    def get(self,request,artist_id):
        try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            artist=admin_models.artist.objects.get(pk=artist_id)
            artist.follow_by.add(requstuser.id)
            artist.save()
            return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_200_OK) 
        except Exception as e:
            return  Response({'success':'false',
                                'error_msg':'invalid id/artist not exists',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)

# user can unfollow a artist
class Artist_Unfollow_By_User(APIView):
    def get(self,request,artist_id):
        try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            artist=admin_models.artist.objects.get(pk=artist_id)
            artist.follow_by.remove(requstuser.id)
            artist.save()
            return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{},
                                    },status=status.HTTP_200_OK) 
        except Exception as e:
            return  Response({'success':'false',
                                'error_msg':'invalid id/artist not exists',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)



#user will download a song

class Download_Song_By_User(APIView):
    @is_authenticate()
    def get(self,request,song_id):
        #try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            
            song=admin_models.songs.objects.get(pk=song_id)
            s3_client=boto3.client("s3")
            r=s3_client.get_object(Bucket="mayanis3",Key="images/songs/song.mp3",aws_acess_key_id='AKIAWZRQG6YB6AULJEWD',aws_secret_acess_key='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')
            d=r["Body"].read()
            print(d)
                

"""
            #=admin_serializers.song_data(song)
           # return Response({'success':f.data})
    

    def post(self,request,path):
            file_path="images/songs"
            if os.path.exists(file_path):
                with open("file_path","rb") as f:
                    return
       
            f=admin_serializers.song_data(song)
            x=f.data["name"]
            print("test",type(song.song_mp3))
            song.downloads.add(requstuser.id)
            song.save()
            return Response({'success':'true',
                                    'error_msg':'',
                                    'errors':{},
                                    'response':{"g":x},
        
                                    },status=status.HTTP_200_OK) 
                                    

        except Exception as e:
            return  Response({'success':'false',
                                'error_msg':'invalid id',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
                                
                                

"""
#to get latest song of a particular artist
class Artist_Latest_Songs(APIView):
    @is_authenticate()
    def get(self,request):
        f1=admin_serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    
    @is_authenticate()
    def post(self, request):
        artist_id=request.data["artist_id"]
        f1=admin_serializers.search(data=request.POST)
        f2=admin_serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            return Response({'success':'false',
                            'error_msg':'invalid_input',
                            'errors':{},
                            'response':{**dict(f1.errors),**dict(f2.errors)},
                            },status=status.HTTP_400_BAD_REQUEST)
        search=request.data["search"] 
        if search!="":
            
        
            result=list(admin_models.songs.objects.filter((Q(artist__pk=artist_id,year__gte=timezone.now()-timedelta(days=30))&(Q(name__icontains=search)|Q(artist__name__icontains=search)|Q(album__name__icontains=search)))).distinct())
        else:   
            result=list(admin_models.songs.objects.filter(artist__pk=artist_id,year__gte=timezone.now()-timedelta(days=30)))
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
                result=result.order_by(order)
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        f1=admin_serializers.User_Liked_Songs_By_Admin(result,many=True)
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



# to get all latest songs

class All_Latest_Songs(APIView):
    @is_authenticate()
    def get(self,request):
        f1=admin_serializers.search()
        f2=serializers.pagination()
        return Response({**f1.data,**f2.data,
                            },status=status.HTTP_202_ACCEPTED)
    
    @is_authenticate()
    def post(self, request):
       
        f1=admin_serializers.search(data=request.POST)
        f2=admin_serializers.pagination(data=request.POST)
        if not(f1.is_valid() and f2.is_valid()):
            return Response({'success':'false',
                            'error_msg':'invalid_input',
                            'errors':{},
                            'response':{**dict(f1.errors),**dict(f2.errors)},
                            },status=status.HTTP_400_BAD_REQUEST)
        search=request.data["search"] 
        if search!="":
            latest_songs=admin_models.songs.objects.filter(year__gte=timezone.now()-timedelta(days=30))
           
            result=list(admin_models.songs.objects.filter((Q(year__gte=timezone.now()-timedelta(days=30))&(Q(name__icontains=search)|Q(artist__name__icontains=search)|Q(album__name__icontains=search)))).distinct())
        else:   
             result=list(admin_models.songs.objects.filter(year__gte=timezone.now()-timedelta(days=30)))
        if request.POST['order_by']!=None and request.POST['order_by']!='':
            if request.POST['order_by_type']=='dec':
                order='-'+request.POST['order_by']
            else:
                order=request.POST['order_by']
                result=result.order_by(order)
        paginate_result=Paginator(result, int(request.POST['result_limit']))
        p_r=paginate_result.get_page(request.POST['page'])
        f1=admin_serializers.User_Liked_Songs_By_Admin(result,many=True)
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

   
#trending songs on basis of likes
class Trending_Songs(APIView):
    def get(self, request):
        s=admin_models.songs.objects.annotate(x=Count("likes")).order_by("-x")[:4]
        print(s)
        f=serializers.Trending_Song(s,many=True)
        return  Response({'success':'true',
                    'error_msg':'',
                    'errors':{},
                    'response':{"msg":f.data},
                    },status=status.HTTP_200_OK)   
    
        

#user will select max 5 artist
class Preferred_Artist_By_User(APIView):
    @is_authenticate()
    def get(self, request):
        artist=admin_models.artist.objects.all()
        f=admin_serializers.Artist_Data(artist,many=True)
        return Response({'success':'true',
                        'error_msg':'',
                        'errors':{},
                        'response':{"artist":f.data},
                        },status=status.HTTP_200_OK) 
    


    @is_authenticate()
    def post(self, request):
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        a=admin_models.artist.objects.get(pk=request.data["artist_id"])
        if len(admin_models.artist.objects.filter(preferred_by=requstuser.id))>=5:
            return Response({'success':'false',
                            'error_msg':'you can prefer max 3 artist',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST) 
            
              
 
#user will select max 5 album       
class Preferred_Album_By_User(APIView):
    @is_authenticate()
    def get(self, request):
        album=admin_models.album.objects.all()
        f=admin_serializers.Album_data(album,many=True)
        return Response({'success':'true',
                        'error_msg':'',
                        'errors':{},
                        'response':{"album":f.data},
                        },status=status.HTTP_200_OK)  


    @is_authenticate()
    def post(self, request):
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        a=admin_models.album.objects.get(pk=request.data["album_id"])
        if len(admin_models.album.objects.filter(preferred_by=requstuser.id))>=5:
            return Response({'success':'false',
                            'error_msg':'you can prefer max 3 album',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST) 
        
        a.preferred_by.add(requstuser.id)
        a.save()
        return Response({'success':'true',
                        'error_msg':'',
                        'errors':{},
                        'response':{},
                        },status=status.HTTP_200_OK)     


#user will select max 100 playlist
class Preferred_Playlist_By_User(APIView):
    @is_authenticate()
    def get(self, request):
        platlist=admin_models.playlist_admin.objects.all()
        f=admin_serializers.playlist_admin_data(platlist,many=True)
        return Response({'success':'true',
                        'error_msg':'',
                        'errors':{},
                        'response':{"playlist":f.data},
                        },status=status.HTTP_200_OK)  

    @is_authenticate()
    def post(self, request):
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        p=admin_models.playlist_admin.objects.get(pk=request.data["playlist_id"])
        if len(admin_models.playlist_admin.objects.filter(preferred_by=requstuser.id))>=100:
            return Response({'success':'false',
                            'error_msg':'you can prefer max 100 playlist',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST) 
        
        p.preferred_by.add(requstuser.id)
        p.save()
        return Response({'success':'true',
                        'error_msg':'',
                        'errors':{},
                        'response':{},
                        },status=status.HTTP_200_OK) 
   

#remove  artist,album,palylist from preferred list
class Remove_Preferred(APIView):
    #use get method to remove artist from preferred list
    @is_authenticate()
    def delete(self,request):
        try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            a=admin_models.artist.objects.get(pk=request.data["artist_id"])
            a.preferred_by.remove(requstuser.id)
            a.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'success':'false',
                            'error_msg':'artist_id not exists',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST) 
      
    #use post method to remove album from preferred list
    @is_authenticate()   
    def post(self,request):
        try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            a=admin_models.album.objects.get(pk=request.data["album_id"])
            a.preferred_by.remove(requstuser.id)
            a.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'success':'false',
                            'error_msg':'album_id not exists',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST) 

     #use put method to remove playlist from preferred list
    @is_authenticate()
    def put(self,request):
        try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            p=admin_models.playlist_admin.objects.get(pk=request.data["playlist_id"])
            p.preferred_by.remove(requstuser.id)
            p.save()
            return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'success':'false',
                            'error_msg':'playlist_id not exists',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_400_BAD_REQUEST) 


    @is_authenticate()
    def post(self, request):
        data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
        requstuser=tools.get_user(*data)
        X1=serializers.User_feed_back(data=request.POST)
        if X1.is_valid():
            u=X1.save()
            u.user=requstuser
            u.save()
            return Response({'success':'true',
                                'error_msg':'',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_200_OK)
        return Response({'success':'false',
                                'error_msg':'',
                                'errors':{**dict(X1.errors)},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)


class User_Current_Subscription_Plan(APIView):
    @is_authenticate()
    def get(self,request,pk):
        try:
            data=tools.decodetoken(request.META['HTTP_AUTHORIZATION'])
            requstuser=tools.get_user(*data)
            data=admin_models.Subscription_History.objects.filter(user=pk).latest("expire")
            f1=admin_serializers.Admin_User_Subscription_Plan(data)
            if data.user==requstuser:
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
            return Response({'success':'false',
                            'error_msg':'USER does not exist',
                            'errors':{},
                            'response':{}
                            },status=status.HTTP_400_BAD_REQUEST) 
        except Exception as ex:
            return Response({'success':'false',
                    'error_msg':'id is not valid or data not exist',
                    'errors':{},
                    'response':{}
                    },status=status.HTTP_400_BAD_REQUEST)




#-------- APIs for Charts of GENREs ----------
class Genre_Charts(APIView):
    def get(self, request):
        data = admin_models.Generes.objects.all()

        return Response({'success':'true',
                        'error_msg':'',
                        'errors':{},
                        'response':{"data": admin_serializers.Genere_Serializer(data, many=True).data},
                        },status=status.HTTP_200_OK) 


    def post(self, request):

        f1 = serializers.Genre_Chart_Serializer(data=request.data)

        if not f1.is_valid():
            return Response({'success':'false',
                        'error_msg':'Invalid input',
                        'errors':{**dict(f1.errors)},
                        'response':{},
                        },status=status.HTTP_400_BAD_REQUEST) 
                        

        songs = admin_models.songs.objects.filter(genres=request.data['genre_id']).order_by("-no_of_times_played")[:int(request.data['limit'])]

        return Response({'success':'true',
                        'error_msg':'',
                        'errors':{},
                        'response':{"data": admin_serializers.Song_data(songs, many=True).data},
                        },status=status.HTTP_200_OK) 


#-----------