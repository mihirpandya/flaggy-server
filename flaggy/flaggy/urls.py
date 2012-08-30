from django.conf.urls import patterns, include, url
from checkins.views import hello_view, addUser

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    (r'^error/', 'direct_to_template', {'template': 'error.html'}),
    (r'^userAdded/', 'direct_to_template', {'template': 'userAdded.html'}),
	url(r'^$', view=hello_view, name='hello_page'),
	url(r'^addUser/', view=addUser, name='addUser'),
	#url(r'^userAdded/', view=userAdded, name='userAdded')
    # Examples:
    # url(r'^$', 'flaggy.views.home', name='home'),
    # url(r'^flaggy/', include('flaggy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
