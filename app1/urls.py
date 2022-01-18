from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^go$', views.go, name='go'),
    url(r'^godash$', views.godash, name='godash'),
    url(r'^logout$', views.logout, name='logout'),
    url(r'^userprofile/(?P<id>\d+)$', views.userprofile, name='userprofile'),
    url(r'^edituserprofile$', views.edituserprofile, name='edituserprofile'),
    url(r'^updateuserprofile$', views.updateuserprofile, name='updateuserprofile'),


    url(r'^create$', views.create, name='create'),
    url(r'^company$', views.company, name='company'),
    url(r'^register/(?P<id>\d+)$$', views.register, name='register'),
    url(r'^regcomp$', views.regcomp, name='regcomp'),  # company register
    url(r'^login$', views.login, name='login'),


    url(r'^cashposition', views.cashposition, name='cashposition'),
    url(r'^updateaccounts',views.updateaccounts,name='updateaccounts'),
    url(r'^editaccounts',views.editaccounts,name='editaccounts'),
]
