from django.conf.urls import patterns, include, url
from doppio.api.views import *
from doppio.api.redirect import authenticate
from doppio.site.views import *
from doppio.site import *
import doppio

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
	url(r'^$', view=hello_view, name='hello_page'),
	url(r'^add_user', view=add_user, name='add_user'),
    url(r'^add_follow', view=add_follow, name='add_follow'),
    url(r'^followers', view=followers, name='followers'),
    url(r'^following', view=following, name='following'),
    url(r'^check_in', view=check_in, name='check_in'),
    url(r'^approve_request', view=approve_request, name='approve_request'),
    url(r'^unfollow', view=unfollow, name='unfollow'),
    url(r'^approved', view=approved_requests, name='approved_requests'),
    url(r'^retrieve', view=retrieve_f_request, name='retrieve_f_request'),
    url(r'^show_checkins', view=show_checkins, name='show_checkins'),
    url(r'^nearby', view=nearby, name='nearby'),
    url(r'^authenticate', view=authenticate, name='authenticate'),
    url(r'^send_info', view=send_info, name='send_info'),
    url(r'^notify', view=notify, name='notify'),
    url(r'^update_sensitivity', view=update_sensitivity, name='update_sensitivity'),
    url(r'^pending_request', view=pending_request, name='pending_request'),
    url(r'^poke', view=poke, name='poke'),
    url(r'^get_sensitivity', view=get_sensitivity, name='get_sensitivity'),
    url(r'^add_incognito', view=add_incognito, name='add_incognito'),
    #(r'^error/', 'direct_to_template', {'template': 'error.html'}),
    #url(r'^custom/', view=custom, name='custom'),
	#url(r'^userAdded/', view=userAdded, name='userAdded')
    # Examples:
    # url(r'^$', 'flaggy.views.home', name='home'),
    # url(r'^flaggy/', include('flaggy.foo.urls')),


    #url(r'^m/home', view=home_page, name='home_page'),


    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
