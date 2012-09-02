from checkins.models import User, CheckIn, Follow
from checkins.controllers import __add_user, __add_follow, __followers, __check_in, verify_user
from django.utils import simplejson
from django.core import serializers

from django.template import Context, loader
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect

def empty_str(s):
	return (s == None or s == "")

def hello_view(request):
    """ Simple Hello World View """
    t = loader.get_template('helloworld.html')
    c = Context({
        'current_time': datetime.now(),
    })
    return HttpResponse(t.render(c))

def add_user(request):
	if request.method == 'GET':
		
		f_n = request.GET.get('fname')
		l_n = request.GET.get('lname')
		fb_id = request.GET.get('fb_id')
		email = request.GET.get('email')

		if(not(empty_str(f_n)) and not(empty_str(l_n)) and not(empty_str(fb_id)) and not(verify_user(User, fb_id))):
			res = __add_user(f_n,l_n,fb_id, 0000, email)
			return HttpResponse("User created", mimetype='application/json')
		else:
			## We should return friends (you mean followers) if the user already exists ##
			return HttpResponse("Error. User could not be created", mimetype='application/json')

def add_follow(request):
	if request.method == 'GET':
		follower = request.GET.get('f_er')
		followed = request.GET.get('f_ed')

		if(follower != None and followed != None):
			res = __add_follow(follower, followed)
			return HttpResponse(res, mimetype='application/json')
		else: 
			return HttpResponseRedirect('/error/')

	else: return HttpResponseRedirect('/notGETmethod/')

def followers(request):
	if request.method == 'GET':
		u_id = request.GET.get('u_id')
		res = __followers(u_id)

		if len(res):
			return HttpResponse(simplejson.loads(res), mimetype='application/json')
		else:
			return HttpResponse("No followers", mimetype='application/json')
	else: 
		return HttpResponseRedirect('/notGETmethod/')

def check_in(request):
	if request.method == 'GET':
		u_id = request.GET.get('u_id')
		lat = request.GET.get('lat')
		long = request.GET.get('long')
		comm = request.GET.get('comm')
		__check_in(long, lat, u_id, comm)
		return HttpResponse("Check-ed In", mimetype='application/json')
	else: 
		return HttpResponseRedirect('/notGETmethod/')

