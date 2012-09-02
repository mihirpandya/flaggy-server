from checkins.models import User, CheckIn, Follow
from checkins import controllers
from django.utils import simplejson
from json import loads, dumps
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

		if(controllers.verify_user(User, fb_id)):
			u = User.objects.get(fb_id=fb_id)
			return HttpResponse("{u_id: "+str(u.u_id)+"}", mimetype='application/json')

		else:
			if(not(empty_str(f_n)) and not(empty_str(l_n)) and not(empty_str(fb_id))):
				res = controllers.__add_user(f_n,l_n,fb_id, 0000, email)
				return HttpResponse(res, mimetype='application/json')
			else:
				## We should return friends (you mean followers) if the user already exists ##
				return HttpResponse("Error. User could not be created", mimetype='application/json')

def add_follow(request):
	if request.method == 'GET':
		follower = request.GET.get('f_er')
		followed = request.GET.get('f_ed')

		if(follower != None and followed != None):
			res = controllers.__add_follow(follower, followed)
			return HttpResponse(res, mimetype='application/json')
		else: 
			return HttpResponseRedirect("Error. Did not find either user.", mimetype='application/json')

	else: return HttpResponseRedirect("No request received.", mimetype='application/json')

def followers(request):
	if request.method == 'GET':
		u_id = request.GET.get('u_id')
		res = controllers.__followers(u_id)

		if len(res):
			return HttpResponse(dumps(res), mimetype='application/json')
		else:
			return HttpResponse("No followers", mimetype='application/json')
	else: 
		return HttpResponseRedirect("No request received.", mimetype='application/json')

def following(request):
	if request.method == 'GET':
		u_id = request.GET.get('u_id')
		res = controllers.__following(u_id)

		if len(res):
			return HttpResponse(dumps(res), mimetype='application/json')
		else:
			return HttpResponse("No followers", mimetype='application/json')
	else: 
		return HttpResponseRedirect("No request received.", mimetype='application/json')		

def check_in(request):
	if request.method == 'GET':
		u_id = request.GET.get('u_id')
		lat = request.GET.get('lat')
		long = request.GET.get('long')
		comm = request.GET.get('comm')
		controllers.__check_in(long, lat, u_id, comm)
		return HttpResponse("Checked In", mimetype='application/json')
	else: 
		return HttpResponseRedirect("No request received.", mimetype='application/json')

