from checkins.models import User, CheckIn, Follow
from checkins.controllers import __addUser

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

# CRUD

def addUser(request):
	if request.method == 'GET':
		
		f_n = request.GET.get('fname')
		l_n = request.GET.get('lname')
		fb_id = request.GET.get('fb_id')
		email = request.GET.get('email')

		if(f_n != None and l_n != None and fb_id != None and not(verifyUser(User, fb_id))):
			__addUser(f_n,l_n,fb_id, 0000, email)
			return HttpResponseRedirect('/userAdded/')
		else:
			return HttpResponseRedirect('/error/')
		# handle request

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
