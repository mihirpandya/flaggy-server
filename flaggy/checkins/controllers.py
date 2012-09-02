from checkins.models import User, CheckIn, Follow
from datetime import datetime
from django.utils import simplejson
from django.core import serializers


def verify_user(obj, value):
	try:
		obj.objects.get(fb_id=value)
		return True
	except obj.MultipleObjectsReturned:
		return True
	except obj.DoesNotExist:
		return False

def __add_user(f_n, l_n, fb, twitter, email):
	d = str(datetime.date(datetime.now()))
	try:
		u = User(fname=f_n, lname=l_n, fb_id=fb, twitter_id=twitter, email=email)
		u.save()
		return "/userAdded/"
	except:
		return "/error/"

def __add_follow(follower, followed):
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

	json_serializer = serializers.get_serializer("json")()

	try:
		user = User.objects.get(pk=u_id)
		foll_list = json_serializer.serialize(Follow.objects.filter(following_id=u_id), ensure_ascii=False)
		
		##for i in f_ers:
		##	foll_list[i] = f_ers[i].following

		return foll_list

	except User.DoesNotExist:
		return "userNotFound"
	except:
		return "error in __followers"

def __check_in(long, lat, u_id, comm):
	d = datetime.now()
	user = User.objects.get(pk=u_id)
	ci = CheckIn(longitude = long,
				 latitude = lat,
				 u_id = user,
				 when = d,
				 comment = comm)
	ci.save()

	return "ok"

