from django.urls import path
from . import views
urlpatterns=[
    path("cms<name>",views.Cms.as_view(),name="Cms"),
    path("Faq",views.Faq_section.as_view(),name="faq_section"),
    path("Faq<pk>",views.Faq_section.as_view(),name="faq_section"),
    path("feedback",views.User_Feedback.as_view(),name="feedback"),
    path("User_Current_Subscription_Plan<pk>",views.User_Current_Subscription_Plan.as_view(),name="User_Current_Subscription_Plan"),
    path("recomended_playlist",views.recomended_playlist.as_view(),name='recomended_playlist'),
    path("recomended_artist<id>",views.recomended_artist.as_view(),name="recomended_artist"),
    path("Song_search",views.Songs_search.as_view(),name='Song_search'),
    path('Albums_Songs/<pk>',views.Albums_songs.as_view(),name='Albums_Songs'),

    # path("",views..as_view(),name='')
    # path("",views..as_view(),name='')
    # path("",views..as_view(),name='')
    
  
    
    path("edit_user_profile",views.Edit_User_Profile.as_view(),name="edit_user_profile"),
    path("change_user_password",views.Change_User_Password.as_view(),name="change_user_password"),
    path("create_playlist",views.Create_Playlist.as_view(),name="create_playlist"),
    path("add_song_playlist",views.Add_Song_Playlist.as_view(),name="add_song_playlist"),
    path("remove_song_playlist",views.Remove_Song_Playlist.as_view(),name="remove_song_playlist"),
    path("Delete_playlist",views.User_delete_playlist.as_view(),name="Delete_playlist"),
    path("artist_albumlist<pk>",views.Aritst_All_Albums_List.as_view(),name="artist_albumlist"),
    path("artist_playlist<pk>",views.Aritst_All_Playlist_List.as_view(),name="artist_playlist_list"),
    path("artist_songlist<pk>",views.Artist_Song_List.as_view(),name="artist_song_list")
   
    ]
