from django.conf.urls import patterns, include, url
from doppio.api.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    (r'^error/', 'direct_to_template', {'template': 'error.html'}),
	url(r'^$', view=hello_view, name='hello_page'),
	url(r'^add_user/', view=add_user, name='add_user'),
    url(r'^add_follow/', view=add_follow, name='add_follow'),
    url(r'^followers/', view=followers, name='followers'),
    url(r'^following/', view=following, name='following'),
    url(r'^check_in/', view=check_in, name='check_in'),
    url(r'^approve_request/', view=approve_request, name='approve_request'),
    url(r'^unfollow/', view=unfollow, name='unfollow'),
    url(r'^unapproved/', view=unapproved_requests, name='unapproved_requests'),
    url(r'^retrieve/', view=retrieve_f_request, name='retrieve_f_request'),
    #url(r'^custom/', view=custom, name='custom'),
	#url(r'^userAdded/', view=userAdded, name='userAdded')
    # Examples:
    # url(r'^$', 'flaggy.views.home', name='home'),
    # url(r'^flaggy/', include('flaggy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
