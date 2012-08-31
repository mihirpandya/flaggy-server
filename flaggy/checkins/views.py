from checkins.models import User, CheckIn, Follow
from checkins.controllers import __addUser, __addFollow, __followers, verifyUser
from django.utils import simplejson
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

def empty_str(s):
	return (s == None or s == "")

# CRUD

def addUser(request):
	if request.method == 'GET':
		
		f_n = request.GET.get('fname')
		l_n = request.GET.get('lname')
		fb_id = request.GET.get('fb_id')
		email = request.GET.get('email')

		if(not(empty_str(f_n)) and not(empty_str(l_n)) and not(empty_str(fb_id)) and not(verifyUser(User, fb_id))):
			res = __addUser(f_n,l_n,fb_id, 0000, email)
			return HttpResponse("User created", mimetype='application/json')
		else:
			## We should return friends if the user already exists ##
			return HttpResponse("Error. User could not be created", mimetype='application/json')

	else: return HttpResponseRedirect('/notGETmethod/')
		# handle request

def addFollow(request):
	if request.method == 'GET':
		follower = request.GET.get('f_er')
		followed = request.GET.get('f_ed')

#		if(not(empty_str(follower)) and not(empty_str(followed))):
		if(follower != None and followed != None):
			res = __addFollow(follower, followed)
			return HttpResponseRedirect(res)
		else: 
			return HttpResponseRedirect('/error/')

	else: return HttpResponseRedirect('/notGETmethod/')

def followers(request):
	if request.method == 'GET':
		u_id = request.GET.get('u_id')
		res = __followers(u_id)
		data = serializers.serialize('json', res)
		return HttpResponse(data, mimetype='application/json')
	else: return HttpResponseRedirect('/notGETmethod/')


def checkIn(long, lat, user, comm):
	d = datetime.datetime.now()
	uid = user.u_id

	ci = CheckIn(longitude = long,
				 latitude = lat,
				 u_id = user,
				 when = d,
				 comment = comm)
	
	ci.save()


# Create your views here.
