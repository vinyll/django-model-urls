from django.conf.urls import patterns, url, include
from django.http import HttpResponse


def dummy_view():
    return HttpResponse("User-agent: *\nDisallow: /", mimetype="text/plain")


app_patterns = patterns('',
    url(r'^about/(?P<pk>\d+)/$', dummy_view, name='pk_path'),
)

urlpatterns = patterns('',
    url(r'^path/$', lambda r: HttpResponse(""), name='basic_path'),
    url(r'^path/(?P<name>[\w-]+)/$', dummy_view, name='url_name'),
    url(r'^path/(?P<name>[\w-]+)/(?P<subref>[\w-]+)/(?P<pk>\d+)/$',
        dummy_view, name='url_mixed'),
    url(r'^app/', include(app_patterns, namespace='app')),
)
