from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    #(r'^flahoo/', include('flahoo.foo.urls')),
    #(r'^[a-z]+/?', 'flahoo.flickr.views.photos'),
	(r'^/?$', 'flahoo.photos.views.index'),
    (r'^public/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/path/to/public/'}),

    # Uncomment the next line to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line for to enable the admin:
    # (r'^admin/(.*)', admin.site.root),
)
