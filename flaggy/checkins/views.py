from checkins.models import User, CheckIn, Follow

from django.template import Context, loader
from datetime import datetime
from django.http import HttpResponse

def hello_view(request):
    """ Simple Hello World View """
    t = loader.get_template('helloworld.html')
    c = Context({
        'current_time': datetime.now(),
    })
    return HttpResponse(t.render(c))

# CRUD

def __addUser(f_n, l_n, fb, twitter):
	if()
	u = User(fname=f_n, lname=l_n, fb_id=fb, twitter_id=twitter)
	u.save()

def addUser(request):
	if request.method == 'GET':
		f_n = request.GET.get('fname')
		l_n = request.GET.get('lname')
		fb_id = request.GET.get('fb_id')
		if(f_n != None and l_n != None and fb_id != None):
			__addUser(f_n,l_n,fb_id, 0000) # Assuming giving less inputs automatically 
					  					   # makes last inputs null

		# handle request
		return HttpResponseRedirect('/userAdded/')

def userAdded():
	t = loader.get_template('userAdded.html')
	return HttpResponse(t.render())

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
