from django.urls import path
from . import views
urlpatterns=[
    path("recomended_playlist",views.recomended_playlist.as_view(),name='recomended_playlist')
    # path("",views..as_view(),name='')
    # path("",views..as_view(),name='')
    # path("",views..as_view(),name='')
    ]
