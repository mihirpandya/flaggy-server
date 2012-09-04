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
	d = datetime.now()
	try:
		u = User(fname=f_n, lname=l_n, fb_id=fb, twitter_id=twitter, email=email, date_joined=d)
		u.save()
		return str(u.pk)
	except:
		return "Error. User could not be created. Problem with __add_user."

def __add_follow(follower, followed):
	try:
		f_er = User.objects.get(pk=follower)
		f_ed = User.objects.get(pk=followed)
		f = Follow(follower=f_er, following=f_ed)
		f.save()
		return "Following "+f_ed.fname
	except User.DoesNotExist:
		return "User does not exist."
	except:
		return "Error. Could not follow "+f_er.fname

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
		return "Error. User does not exist."

def __following(u_id):
	try: 
		following_list = Follow.objects.filter(follower_id=u_id)
		array = []
		for item in following_list:
			dict_user = { }
			dict_user['u_id'] = item.following.pk
			dict_user['name'] = item.following.fname + " " + item.following.lname
			dict_user['location'] = last_check_in(item.follower.pk)
			array.append(dict_user)

		return array

	except User.DoesNotExist:
		return "Error. User does not exist."

def __check_in(long, lat, u_id, comm):
	d = datetime.now()
	user = User.objects.get(pk=u_id)
	print lat
	print long
	ci = CheckIn(longitude = long,
				 latitude = lat,
				 u_id = user,
				 when = d,
				 comment = comm)
	ci.save()

	return "ok"


## HELPERS ##
## Here will be the functions that are not directly mapped to a view ##

def last_check_in(user_id):
	try:
		checkin = CheckIn.objects.filter(u_id = user_id).latest('when')
		coor = { }
		coor["long"] = str(checkin.longitude)
		coor["lat"] = str(checkin.latitude)

		return coor
	except CheckIn.DoesNotExist:
		return None
