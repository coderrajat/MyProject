from os import name
from django.urls import path
from . import views
urlpatterns=[
    path("cms<name>",views.cms.as_view(),name='cms'),
    path("image_settings",views.image_settings.as_view(),name='image_settings'),
    path("smtp_settings_api",views.smtp_settings_api.as_view(),name='smtp_settings_api'),
    path("social_media_settings",views.social_media_settings.as_view(),name='social_media_settings'),
    path("general_settings_api",views.general_settings_api.as_view(),name='general_settings_api'),
    path("admin_profile",views.admin_profile.as_view(),name='admin_profile'),
    path("change_admin_password",views.change_admin_password.as_view(),name='change_admin_password'),
    path("search_consumer_api",views.search_consumer_api.as_view(),name='search_consumer_api'),
    path("edit_user_api<id>",views.edit_user_api.as_view(),name='edit_user_api'),
    path("delete_user<id>",views.delete_user.as_view(),name='delete_user'),
    path("subadmin_list",views.subadmin_list.as_view(),name='subadmin_list'),
    path("edit_subadmin<id>",views.edit_subadmin.as_view(),name='edit_subadmin'),
    path("delete_subadmin<id>",views.delete_subadmin.as_view(),name='delete_subadmin'),
    path("block_subadmin<id>",views.block_subadmin.as_view(),name='block_subadmin'),
    path("song_search_list",views.song_search_list.as_view(),name='song_search_list'),
    path("get_playlist_admin",views.get_playlist_admin.as_view(),name='get_playlist_admin'),
    path("get_songs_admin_playlist/<id>",views.get_song_admin_playlist.as_view(),name='get_playlist_admin'),
    
    # sonu album path
    #path("album",views.album.as_view(),name='album'),
    #path('album/<id>', views.album.as_view()),
  
    #album api
    path('album_api', views.albumAPI.as_view(),name='album_api'),
    path('album_api/<id>', views.albumAPI.as_view(),name='album_api'),
    #Dashboard api
    path('dash_board', views.dash_board.as_view(),name='dash_board'),
    #Album_search api
    path("album_search",views.album_search.as_view(),name='album_search'),
    #Albums_song api
    path('albums_song',views.song_album.as_view(),name='albums_song'),
    path('albums_song/<pk>',views.song_album.as_view(),name='albums_song'),
    #albums_song search api
    path('albums_song_search/<pk>',views.albums_song_search_list.as_view(),name='albums_song_search'),
    #path('albums_song_search',views.albums_song_search_list.as_view(),name='albums_song_search'),

    #path('get_songs',views.get_songs.as_view(),name='get_songs'),
    #path('get_songs/<pk>',views.get_songs.as_view(),name='get_songs'),

    #path("playlist_admin/<int:id>",views.playlist_admin_by_id.as_view(),name='playlist_admin'),
    #path("playlist_admin",views.playlist_adminn.as_view(),name='playlist_admin'),
    path("playlist_admin",views.playlist_admin_get.as_view(),name='playlist_admin_get'),
    path("playlist_admin/<id>",views.playlist_admin.as_view(),name='playlist_admin'),
    #path("playlist_admin/<id>",views.get_song_admin_playlist.as_view(),name='playlist_admin'),

#   path("playlist_admin/remove/id",views.playlist_admin.as_view(), name='playlist_admin)

    path("playlist_all/<id>/remove/",views.playlist_admin_removesong.as_view(),name='playlist_admin'),
    
    #path("playlist_all",views.playlist_by_id.as_view(),name='playlist_admin'),
    
    #path("playlist_admin/all",views.playlist_adminget.as_view(),name='playlist_admin'), #getting all playlist

    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    #
    path("artist_data",views.Artist_api.as_view(),name="artist_data"),
    path("artist_data<pk>",views.Artist_api.as_view(),name="artist_data1"),
    path("subscription_data",views.SubscriptionPlan_api.as_view(),name="subscription_data"),
    path("subscription_data<pk>",views.SubscriptionPlan_api.as_view(),name="subscription_data1"),
    path("notification_data",views.Notification_api.as_view(),name="notification_data"),
    path("notification_data<pk>",views.Notification_api.as_view(),name="notification_data1"),
    path("artist_search_list",views.Artist_search_list.as_view(),name="artist_search_list"),
    path("artist_search_list<pk>",views.Artist_search_list.as_view(),name="artist_search_list"),
    path("artist_album<pk>",views.Artist_album_data.as_view(),name="artist_album"),
    path("artist_album",views.Artist_album_data.as_view(),name="artist_album1"),
    path("song_data<pk>",views.Song_api.as_view(),name="song_data"),
    path("song_data",views.Song_api.as_view(),name="song_data1"),
    path("artist_song<pk>",views.Artist_song_data.as_view(),name="artist_album"),
    path("artist_song",views.Artist_song_data.as_view(),name="artist_album1"),
    path("artist_search_album<pk>",views.Artist_album_search_list.as_view(),name="artist"),
    path("artist_search_album",views.Artist_album_search_list.as_view(),name="artist"),
    path("artist_Song_search",views.Artist_song_search_list.as_view(),name="artist"),
    path("artist_Song_search<pk>",views.Artist_song_search_list.as_view(),name="artist"),
   # path("artistalbum_search_song<pk>",views.Artist_album_song_search_list.as_view(),name="artist"),
    path("artistalbum_search_song",views.Artist_album_song_search_list.as_view(),name="artist"),
    #sonu
   
    
    
 
    
    
    ]
#handler404 = 'admins.views.error_404_view'