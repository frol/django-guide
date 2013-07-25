try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url # Django < 1.4

urlpatterns = patterns('guide.views',
    url('^toggle/(?P<status>enable|disable)/$', 'toggle_guides', name='toggle_guides'),
) 
