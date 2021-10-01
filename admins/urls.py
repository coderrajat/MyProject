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
    path("delete_user",views.delete_user.as_view(),name='delete_user'),
    path("subadmin_list",views.subadmin_list.as_view(),name='subadmin_list'),
    path("edit_subadmin<id>",views.edit_subadmin.as_view(),name='edit_subadmin'),
    path("delete_subadmin<id>",views.delete_subadmin.as_view(),name='delete_subadmin'),
    path("block_subadmin<id>",views.block_subadmin.as_view(),name='block_subadmin'),
    path("song_search_list",views.song_search_list.as_view(),name='song_search_list'),
    path("get_playlist_admin",views.get_playlist_admin.as_view(),name='get_playlist_admin'),
    #path("playlist_admin/<int:id>",views.playlist_admin_by_id.as_view(),name='playlist_admin'),
    #path("playlist_admin",views.playlist_adminn.as_view(),name='playlist_admin'),
    path("playlist_admin",views.playlist_admin_get.as_view(),name='playlist_admin_get'),
    path("playlist_admin/<id>",views.playlist_adminn.as_view(),name='playlist_admin'),


    #path("playlist_all",views.playlist_by_id.as_view(),name='playlist_admin'),
    

  #  path("playlist_admin/all",views.playlist_adminget.as_view(),name='playlist_admin'), #getting all playlist

    


    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    #
    ]
#handler404 = 'admins.views.error_404_view'