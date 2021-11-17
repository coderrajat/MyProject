
from django.urls import path

from . import views
app_name='account'
urlpatterns=[
    path('login_admin_api',views.login_admin_api.as_view(),name='login_admin_api'),
    # path("login_admin_api",views.login_admin_api.as_view(),name='login_admin_api'),
    path("logout_api",views.logout_api.as_view(),name='logout_api'),
    path("signup_user",views.signup_user.as_view(),name='signup_user'),
    path("check_user_otp",views.check_user_otp.as_view(),name='check_user_otp'),
    path("create_password",views.create_password.as_view(),name='create_password'),
    path("signin_user",views.signin_user.as_view(),name='signin_user'),
    path("get_email",views.get_email.as_view(),name='get_email'),
    path("check_admin_otp",views.check_admin_otp.as_view(),name='check_admin_otp'),
    path("change_password_admin",views.change_password_admin.as_view(),name='change_password_admin'),
    # path("login_admin_api",views.login_admin_api.as_view(),name='login_admin_api'),
    # path("login_admin_api",views.login_admin_api.as_view(),name='login_admin_api'),
    # path("login_admin_api",views.login_admin_api.as_view(),name='login_admin_api'),
    # path("login_admin_api",views.login_admin_api.as_view(),name='login_admin_api'),
    # path("login_admin_api",views.login_admin_api.as_view(),name='login_admin_api'),
    # path("login_admin_api",views.login_admin_api.as_view(),name='login_admin_api'),
    # path("login_admin_api",views.login_admin_api.as_view(),name='login_admin_api'),
    #path('all_users', views.userall_data.as_view()),
    ]
