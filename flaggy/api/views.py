from checkins.models import User, CheckIn, Follow
from checkins.controllers import *
from django.utils import simplejson
from json import loads, dumps
from django.core import serializers

from django.template import Context, loader
from datetime import datetime
from django.http import HttpResponse, HttpResponseRedirect

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

		res = { }
		checkin_user = { }

		if (controllers.verify_user(fb_id)):
			u = User.objects.get(fb_id=fb_id)

			c = CheckIn.objects.filter(u_id_id = u.u_id)

			if(len(c)):
				last_checkin = c[(len(c)-1)]

				checkin_user["longitude"] = int(last_checkin.longitude)
				checkin_user["latitude"] = int(last_checkin.latitude)
				checkin_user["when"] = str(last_checkin.when)
				checkin_user["comment"] = str(last_checkin.comment)
				
			res["status"] = 2
			res["last_checkin"] = checkin_user
			## Add the last checkin location here
			res["u_id"] = str(u.u_id)

#			return HttpResponse(dumps(res), mimetype='application/json')

		elif (not(empty_str(f_n)) and not(empty_str(l_n)) and not(empty_str(fb_id))):
			res["status"] = 1
			res["u_id"] = controllers.__add_user(f_n,l_n,fb_id, 0000, email)
			
#			return HttpResponse(dumps(res), mimetype='application/json')
		else:
			res["status"] = 0
			## We should return friends (you mean followers) if the user already exists ##
		
		return HttpResponse(dumps(res), mimetype='application/json')

def add_follow(request):
	if request.method == 'GET':
		follower = request.GET.get('f_er')
		followed = request.GET.get('f_ed')

		if(follower != None and followed != None):
			res = controllers.__add_follow(follower, followed)
			return HttpResponse(res, mimetype='application/json')
		else: 
			return HttpResponse("Error. Did not find either user.", mimetype='application/json')

	else: return HttpResponse("No request received.", mimetype='application/json')

def approve_request(request):
	if request.method == 'GET':
		key = request.GET.get('k')

		res = controllers.__approve_request(key)

		return HttpResponse(res, mimetype='application/json')

def unfollow(request):
	if request.method == 'GET':
		f_er = request.GET.get('f_er')
		f_ed = request.GET.get('f_ed')

		res = controllers.__unfollow(f_er, f_ed)

		return HttpResponse(res, mimetype='application/json')

def followers(request):
	if request.method == 'GET':
		u_id = request.GET.get('u_id')
		res = controllers.__followers(u_id)

		if len(res):
			return HttpResponse(dumps(res), mimetype='application/json')
		else:
			return HttpResponse("No followers", mimetype='application/json')
	else: 
		return HttpResponse("No request received.", mimetype='application/json')

def following(request):
	if request.method == 'GET':
		u_id = request.GET.get('u_id')
		res = controllers.__following(u_id)
		if len(res):
			return HttpResponse(dumps(res), mimetype='application/json')
		else:
			return HttpResponse("Following no one", mimetype='application/json')
	else: 
		return HttpResponse("No request received.", mimetype='application/json')		

def check_in(request):
	if request.method == 'GET':
		u_id = request.GET.get('u_id')
		lat = request.GET.get('lat')
		lon = request.GET.get('long')
		comm = request.GET.get('comm')

		controllers.__check_in(lon, lat, u_id, comm)
		return HttpResponse("Checked In", mimetype='application/json')
	else: 
		return HttpResponse("No request received.", mimetype='application/json')

