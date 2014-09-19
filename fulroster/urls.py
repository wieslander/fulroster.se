from django.conf.urls import patterns, include, url

import fulroster.views
import parties.urls

urlpatterns = patterns('',
    url(r'^$', fulroster.views.index, name='home'),
    url(r'^om/$', fulroster.views.about, name='about'),
    url(r'^partier/', include(parties.urls, namespace='parties')),
)
