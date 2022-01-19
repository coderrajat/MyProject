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
    
  
     #to get all albums of a artist ordering by time
    path("artist_albumlist",views.Aritst_All_Albums_List.as_view(),name="artist_albumlist"),
    # to get all palylist of a artist ordering by time
    path("artist_playlist",views.Aritst_All_Playlist_List.as_view(),name="artist_playlist_list"),
    #to get all songs of a artist ordering by time
    path("artist_songlist",views.Artist_All_Song_List.as_view(),name="artist_song_list"),
    #user dashboard
    path("edit_user_profile",views.Edit_User_Profile.as_view(),name="edit_user_profile"),
    #user can change password if he remembers his password but need to change it
    path("change_user_password",views.Change_User_Password.as_view(),name="change_user_password"),
    path("create_playlist",views.Create_Playlist.as_view(),name="create_playlist"),
    path("add_song_playlist",views.Add_Song_Playlist.as_view(),name="add_song_playlist"),
    path("remove_song_playlist",views.Remove_Song_Playlist.as_view(),name="remove_song_playlist"),
    path("Delete_playlist",views.User_delete_playlist.as_view(),name="Delete_playlist"),
    path("artist_albumlist<pk>",views.Aritst_All_Albums_List.as_view(),name="artist_albumlist"),
    path("artist_playlist<pk>",views.Aritst_All_Playlist_List.as_view(),name="artist_playlist_list"),
    #path("artist_songlist<pk>",views.Artist_Song_List.as_view(),name="artist_song_list"),
   
    # it will show all the liked songs of a user
    path("liked_songs_user",views.User_Liked_Songs.as_view(),name="user_liked_songs"),
    # it will show all the downloaded songs of a user
    path("downloaded_songs_user",views.User_Downloaded_Songs.as_view(),name="user_downloaded_songs"),
    #to get all the created palylist of a user 
    path("user_playlist",views.User_Playlist.as_view(),name="user_playlist"),
    #by this user user can like a song
    path("like_song_by_user/<song_id>",views.Like_Song_By_User.as_view(),name="user_like_song"),
    #by this user user can dislike a song
    path("dislike_song_by_user/<song_id>",views.Dislike_Song_By_User.as_view(),name="dislike_song_by_user"),
     #by this user user can like a song
    path("like_album_by_user/<album_id>",views.Like_Album_By_User.as_view(),name="like_album_by_user"),
     #by this user user can dislike a song
    path("dislike_album_by_user/<album_id>",views.Dislike_Album_By_User.as_view(),name="dislike_album_by_user"),
    
    path("download_song_user/<song_id>",views.Download_Song_By_User.as_view(),name="downnload_song_by_user"),
    #user can folow an artist
    path("artist_follow_by_user/<artist_id>",views.Artist_Follow_By_User.as_view(),name="artist_follow_by_user"),
    path("artist_unfollow_by_user/<artist_id>",views.Artist_Unfollow_By_User.as_view(),name="artist_unfollow_by_user"),
    #path("t/<pk>",views.Artist_Latest_Songs.as_view(),name="artist_latest_songs")
    #
    path("artist_latest_songs",views.Artist_Latest_Songs.as_view(),name="artist_latest_songs"),
    #will show all latest songs
    path("latest_songs",views.All_Latest_Songs.as_view(),name="latest_songs"),
    path("trending_song_by_most_liked",views.Trending_Songs.as_view(),name="trendig_song_by_liked_song"),
    path("preferred_artist_by_user",views.Preferred_Artist_By_User.as_view(),name="preferred_artist_by_user"),
    path("preferred_album_by_user",views.Preferred_Album_By_User.as_view(),name="preferred_album_by_user"),
    path("preferred_playlist_by_user",views.Preferred_Playlist_By_User.as_view(),name="preferred_playlist_by_user"),
    path("remove_preferred",views.Remove_Preferred.as_view(),name="remove_preferred"),
   
    #Genre Charts 
    path("genre_charts",views.Genre_Charts.as_view(),name="genre_charts"),
    ]
