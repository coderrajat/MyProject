from os import name
from django.urls import path

from . import views
urlpatterns=[
    path("cms<name>",views.cms.as_view(),name='cms'),
    path("Faq",views.Faq_section.as_view(),name='faq'),
    path("Faq<pk>",views.Faq_section.as_view(),name='faq'),
    path("image_settings",views.image_settings.as_view(),name='image_settings'),
    path("smtp_settings_api",views.smtp_settings_api.as_view(),name='smtp_settings_api'),
    path("social_media_settings",views.social_media_settings.as_view(),name='social_media_settings'),
    path("general_settings_api",views.general_settings_api.as_view(),name='general_settings_api'),
    path("admin_profile",views.admin_profile.as_view(),name='admin_profile'),
    path("change_admin_password",views.change_admin_password.as_view(),name='change_admin_password'),
    path("search_consumer_api",views.search_consumer_api.as_view(),name='search_consumer_api'),
    path("edit_user_api<id>",views.edit_user_api.as_view(),name='edit_user_api'),
    path("edit_user_api",views.edit_user_api.as_view(),name='edit_user_api'),
    path("block_user_api<id>",views.edit_user_api.as_view(),name='block_user_api'),
    path("delete_user<id>",views.delete_user.as_view(),name='delete_user'),
    path('block_user<id>',views.block_user.as_view(),name='block_user'),
    path("subadmin_list",views.subadmin_list.as_view(),name='subadmin_list'),
    path("edit_subadmin<id>",views.edit_subadmin.as_view(),name='edit_subadmin'),
    path("edit_subadmin",views.edit_subadmin.as_view(),name='edit_subadmin'),
    path("delete_subadmin<id>",views.delete_subadmin.as_view(),name='delete_subadmin'),
    path("add_subadmin",views.Add_Subadmin.as_view(),name='add_subadmin'),
    path("block_subadmin<id>",views.block_subadmin.as_view(),name='block_subadmin'),
    
    path("song_search_list",views.song_search_list.as_view(),name='song_search_list'),
    path("song/<pk>",views.Song_api.as_view(),name="song"),
    
    
    path("song",views.Song_api.as_view(),name="song"),
    path("get_playlist_admin",views.get_playlist_admin.as_view(),name='get_playlist_admin'),
    path("get_songs_admin_playlist/<id>",views.get_song_admin_playlist.as_view(),name='get_playlist_admin'),
    
    #album api
    path('album', views.albumAPI.as_view(),name='album_api'),
    path('album/<pk>', views.albumAPI.as_view(),name='album_api'),
    #Dashboard api
    path('dash_board', views.dash_board.as_view(),name='dash_board'),
    #Album_search api 
    path("album_search",views.album_search.as_view(),name='album_search'),
    #Albums_song api
    path('albums_song',views.song_album.as_view(),name='albums_song'),
    path('albums_song/<pk>',views.song_album.as_view(),name='albums_song'),
    #albums_song search api
    path('albums_song_search/<pk>',views.albums_song_search_list.as_view(),name='albums_song_search'),
    path('song',views.Song_api.as_view(),name='song'),
    path('song/<pk>',views.Song_api.as_view(),name='song'),
   

    #path("playlist_admin/<int:id>",views.playlist_admin_by_id.as_view(),name='playlist_admin'),
    #path("playlist_admin",views.playlist_adminn.as_view(),name='playlist_admin'),
    path("playlist_admin",views.playlist_admin_get.as_view(),name='playlist_admin_get'),
    path("playlist_admin/<id>",views.playlist_admin.as_view(),name='playlist_admin'),
    #path("playlist_admin/<id>",views.get_song_admin_playlist.as_view(),name='playlist_admin'),

#   path("playlist_admin/remove/id",views.playlist_admin.as_view(), name='playlist_admin)

    path("playlist_all/<id>/remove/",views.playlist_admin_removesong.as_view(),name='playlist_admin'),
    path("playlist_all/<id>/add/",views.playlist_admin_addsong.as_view(),name='playlist_admin'),
    
    #path("playlist_all",views.playlist_by_id.as_view(),name='playlist_admin'),
    

    
    #path("playlist_admin/all",views.playlist_adminget.as_view(),name='playlist_admin'), #getting all playlist

    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    #
    path("artist",views.Artist_api.as_view(),name="artist"),
    path("artist/<pk>",views.Artist_api.as_view(),name="artist_data1"),
    path("subscription_data",views.SubscriptionPlan_api.as_view(),name="subscription_data"),
    path("subscription_data/<pk>",views.SubscriptionPlan_api.as_view(),name="subscription_data1"),
    path("notification_data",views.Notification_api.as_view(),name="notification_data"),
    path("notification_data/<pk>",views.Notification_api.as_view(),name="notification_data1"),
    
    
    
    
    
    path("artist_search_list",views.Artist_search_list.as_view(),name="artist_search_list"),
    path("artist_album/<pk>",views.Artist_album_data.as_view(),name="artist_album"),
    path("artist_album",views.Artist_album_data.as_view(),name="artist_album1"),
    path("artist_song",views.Artist_song_data.as_view(),name="artist_album1"),
    path("artist_search_album/<pk>",views.Artist_album_search_list.as_view(),name="artist_search_album"),
    path("artist_search_album",views.Artist_album_search_list.as_view(),name="artist_search_album"),
    path("artist_song_search/<pk>",views.Artist_song_search_list.as_view(),name="songs in artist"),
   # path("artistalbum_search_song<pk>",views.Artist_album_song_search_list.as_view(),name="artist"),
    path("song_in_artist_album",views.Artist_album_song_search_list.as_view(),name="song_in_artist_album"),
    path("artist_remove_song",views.Artist_remove_song.as_view(),name="artist_remove_song"),
    path("artist_remove_album",views.Artist_remove_album.as_view(),name="artist_remove_album"),
    path("create_user_playlist_by_admin",views.Create_User_Playlist_For_Admin.as_view(),name="create_admin_user_playlist"),
    path("user_liked_songs_for_admin/<pk>",views.User_Liked_Songs_By_Admin.as_view(),name="admin_user_liked_songs"),
    path("user_liked_songs_for_admin",views.User_Liked_Songs_By_Admin.as_view(),name="admin_user_liked_songs"),
    path("user_subscription_plan",views.User_Subscription_Plan_History_For_Admin.as_view(),name="admin_user_subscription_plan"),
    path("user_subscription_plan/<pk>",views.User_Subscription_Plan_History_For_Admin.as_view(),name="admin_user_subscription_plan"),
    path("Artist_album_remove_song",views.Artist_Album_Remove_Song.as_view(),name="artist_album_remove_song"),
    path("user_current_subscription_plan/<pk>",views.User_Current_Subscription_Plan.as_view(),name="current_subscription_plan")

   
    
   
   
    
    
    ]
#handler404 = 'admins.views.error_404_view'