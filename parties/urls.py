from django.conf.urls import patterns, url

from parties import views

urlpatterns = patterns('',
    url(r'^$', views.entries, name='entries'),
    url(r'^(?P<id>\d+)/(?P<slug>[A-Za-z0-9_-]*)$', views.show, name='show'),
)
