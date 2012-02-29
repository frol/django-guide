from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('guide.views',
    url('^toggle/(?P<status>enable|disable)/$', 'toggle_guides', name='toggle_guides'),
) 
