from django.urls import path
from . import views
urlpatterns=[
    path("cms",views.cms.as_view(),name='cms'),
    path("image_settings",views.image_settings.as_view(),name='image_settings'),
    path("smtp_settings_api",views.smtp_settings_api.as_view(),name='smtp_settings_api'),
    path("social_media_settings",views.social_media_settings.as_view(),name='social_media_settings'),
    path("general_settings_api",views.general_settings_api.as_view(),name='general_settings_api'),
    path("admin_profile",views.admin_profile.as_view(),name='admin_profile'),
    path("change_admin_password",views.change_admin_password.as_view(),name='change_admin_password'),
    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    # path("cms",views.cms.as_view(),name='cms'),
    #
    ]
