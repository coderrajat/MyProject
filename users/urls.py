from django.urls import path
from . import views
urlpatterns=[
    path("recomended_playlist",views.recomended_playlist.as_view(),name='recomended_playlist'),
    # path("",views..as_view(),name='')
    # path("",views..as_view(),name='')
    # path("",views..as_view(),name='')
    
  
    
    path("edit_user_profile",views.Edit_User_Profile.as_view(),name="edit_user_profile"),
    path("change_user_password",views.Change_User_Password.as_view(),name="change_user_password"),
    path("create_playlist",views.Create_Playlist.as_view(),name="create_playlist"),
    path("add_song_playlist",views.Add_Song_Playlist.as_view(),name="add_song_playlist"),
    path("artist_albumlist<pk>",views.Aritst_All_Albums_List.as_view(),name="artist_albumlist"),
    path("artist_playlist<pk>",views.Aritst_All_Playlist_List.as_view(),name="artist_playlist_list"),
    path("artist_songlist<pk>",views.Artist_Song_List.as_view(),name="artist_song_list"),
    path("liked_songs_user",views.User_Liked_Songs.as_view(),name="user_liked_songs")
   
    ]
