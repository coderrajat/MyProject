from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.paginator import Paginator
from rest_framework import status
from django.db.models import Q
from admins import models as admin_models
from accounts import models as account_models
import bcrypt
from accounts import tools
import datetime
from . import serializers
import random
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
    @is_authenticate
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
                            'response':{'result':serializers.Song_search_data(p_r,many=True).data},
                            'pagination':{'count':len(list(p_r)),
                                        'previous':'true' if p_r.has_previous() else 'false',
                                        'next':'true' if p_r.has_next() else 'false',
                                        'startIndex':p_r.start_index(),
                                        'endIndex':p_r.end_index(),
                                        'totalResults':len(list(result)),
                                },
                            },status=status.HTTP_202_ACCEPTED)

class Albums_songs(APIView):
    @is_authenticate()
    def get(self,request,id):
        if id.isnumeric() !=  True:
            return Response({'success':'false',
                            'error_msg':'ID IS NOT AN INTEGER',
                            'errors':{},
                            'response':{},
                            },status=status.HTTP_404_NOT_FOUND)

        #alb=list(admin_models.album.objects.prefetch_related().filter(id=id))
        alb=list(admin_models.album.objects.filter(songs__album__id=id))
        if alb==[]:
            return Response({'success':'false',
                                'error_msg':'invalid ID',
                                'errors':{},
                                'response':{},
                                },status=status.HTTP_400_BAD_REQUEST)
        alb=alb[0]
        f1=serializers.Albums_songs(alb)
        return Response({'success':'true',
                            'error_msg':'',
                            'errors':{},
                            'response':{"Albums_songs_data":f1.data},
                            },status=status.HTTP_200_OK)    

