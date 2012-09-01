from checkins.models import User, CheckIn, Follow
from datetime import datetime


def verifyUser(obj, value):
	try:
		obj.objects.get(fb_id=value)
		return True
	except obj.MultipleObjectsReturned:
		return True
	except obj.DoesNotExist:
		return False

def __addUser(f_n, l_n, fb, twitter, email):
	d = str(datetime.date(datetime.now()))
	try:
		u = User(fname=f_n, lname=l_n, fb_id=fb, twitter_id=twitter, email=email)
		u.save()
		return "/userAdded/"
	except:
		return "/error/"

def __addFollow(follower, followed):
	try:
		f_er = User.objects.get(pk=follower)
		f_ed = User.objects.get(pk=followed)
		f = Follow(follower=f_er, following=f_ed)
		f.save()
		return "/followAdded/"
	except User.DoesNotExist:
		return "/userNotFound/"
	except:
		return "/error/"

def __followers(u_id):
	try:
		foll_list = Follow.objects.filter(following=u_id)
		
		##for i in f_ers:
		##	foll_list[i] = f_ers[i].following

		return foll_list

	except User.DoesNotExist:
		return "userNotFound"
	except:
		return "error in __followers"

def __checkIn(long, lat, user, comm):
	d = datetime.datetime.now()
	uid = user.u_id
	ci = CheckIn(longitude = long,
				 latitude = lat,
				 u_id = user,
				 when = d,
				 comment = comm)
	
	ci.save()
