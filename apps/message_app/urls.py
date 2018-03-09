from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^newmessage$', views.newmessage, name='newmessage'),
    url(r'^delete/(?P<message_id>\d+)/', views.delete, name='delete'),
    url(r'^like/(?P<message_id>\d+)/', views.like, name='like'),
    url(r'^comment/(?P<id>\d+)/', views.comment, name='comment'),
    url(r'^popular$', views.popular, name='popular'),
    url(r'^popularpage$', views.popularpage, name='popularpage'),
    url(r'^about$', views.about, name='about'),
]
