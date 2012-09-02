import sys
import pprint
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
		u = User(fname=f_n, lname=l_n, fb_id=fb, twitter_id=twitter, email=email, date_joined=d)
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

	try:
		follower_list = Follow.objects.filter(following_id=u_id)
		array = []
		for item in follower_list:
			dict_user = { }
			dict_user['u_id'] = item.follower.pk
			dict_user['name'] = item.follower.fname + " " + item.follower.lname
			array.append(dict_user)

		return array

	except User.DoesNotExist:
		return "userNotFound"

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

