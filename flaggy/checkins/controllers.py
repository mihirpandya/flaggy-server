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
	u = User(fname=f_n, lname=l_n, fb_id=fb, twitter_id=twitter, email=email)
	u.save()
	return None