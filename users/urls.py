from django.urls import path
from . import views
urlpatterns=[
    path("recomended_playlist",views.recomended_playlist.as_view(),name='recomended_playlist'),

    path("Song_search",views.Songs_search.as_view(),name='Song_search'),
    path('Albums_songs<id>',views.Albums_songs.as_view(),name='Albums_songs')

    # path("",views..as_view(),name='')
    # path("",views..as_view(),name='')
    # path("",views..as_view(),name='')
    ]
