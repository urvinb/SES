from django.urls import path, re_path
from institute.views import *
from django.conf.urls import url
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register', register, name="register"),
    path('login', login, name="login"),
    path('logout', logout, name="logout"),
    # url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
    #     activate, name='activate'),
    path('activate/<slug:uidb64>/<slug:token>/', activate, name='activate'),
    path('examform',examform, name="examform"),
    path('',index_institute, name="index_institute"),
    path('update_exam/<int:id>',update_exam, name="update_exam"),
    path('delete_exam/<int:id>',delete_exam, name="delete_exam"),
]
