from checkins.models import User, CheckIn, Follow

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

def verifyUser(obj, value):
	try:
		obj.objects.get(fb_id=value)
		return True
	except obj.MultipleObjectsReturned:
		return True
	except obj.DoesNotExist:
		return False

def __addUser(f_n, l_n, fb, twitter):
	u = User(fname=f_n, lname=l_n, fb_id=fb, twitter_id=twitter)
	u.save()
	return None

def addUser(request):
	if request.method == 'GET':
		
		f_n = request.GET.get('fname')
		l_n = request.GET.get('lname')
		fb_id = request.GET.get('fb_id')

		if(f_n != None and l_n != None and fb_id != None and not(verifyUser)):
			__addUser(f_n,l_n,fb_id, 0000)
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
