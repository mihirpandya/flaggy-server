from django.conf.urls import patterns, include, url
from checkins import views

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('django.views.generic.simple',
    (r'^error/', 'direct_to_template', {'template': 'error.html'}),
	url(r'^$', view=views.hello_view, name='hello_page'),
	url(r'^add_user/', view=views.add_user, name='add_user'),
    url(r'^add_follow/', view=views.add_follow, name='add_follow'),
    url(r'^followers/', view=views.followers, name='followers'),
    url(r'^following/', view=views.following, name='following'),
    url(r'^check_in/', view=views.check_in, name='check_in'),
	#url(r'^userAdded/', view=userAdded, name='userAdded')
    # Examples:
    # url(r'^$', 'flaggy.views.home', name='home'),
    # url(r'^flaggy/', include('flaggy.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
