"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils import unittest
from django.test import TestCase
from django.test.client import Client
from json import loads
from doppio.models import *
from doppio.api.controllers import __add_user as c_add_user
from doppio.api.controllers import __add_follow as c_add_follow
from doppio.api.views import *
from doppio.api.utils import *
from random import random
from datetime import datetime

c = Client()

class ControllerAddUserTestCase(unittest.TestCase):
	def setUp(self):
		self.fb_id = int(random()*100000000)
		self.testUser = User(fname="Automated",
			                 lname="Tester",
			                 fb_id=self.fb_id,
			                 twitter_id=0,
			                 email="me@mihirmp.com",
			                 date_joined=datetime.now(),
			                 distance_sensitivity=1)

		self.token = "random string that can be a hashed token"
		self.device = "iPhone"

	def testAddUser(self):
		response_user = c.post('/add_user/', {'fname': "Automated", 
			                  'lname': "Tester",
			                  'fb_id': self.fb_id,
			                  "email": "me@mihirmp.com"})

		u = User.objects.get(fb_id=self.fb_id)

		response_token = c.post('/add_token/', {"u_id": u.u_id,
			                                   "device": self.device,
			                                   "tok": self.token})
		
		t = UserTokens.objects.get(u_id=u.u_id)

		self.assertEquals(response_user.status_code, 200)
		self.assertEquals(u.fname, self.testUser.fname)
		self.assertEquals(u.lname, self.testUser.lname)
		self.assertEquals(u.email, self.testUser.email)
		self.assertEquals(t.u_id.u_id, u.u_id)
		self.assertEquals(t.token, self.token)
		self.assertEquals(t.device, self.device)

class ControllerFollowTestCase(unittest.TestCase):
	def setUp(self):
		self.fb_id1 = int(random()*100000000)
		self.fb_id2 = int(random()*100000000)
		self.testUser1 = User(fname="Automated1",
			                 lname="Tester1",
			                 fb_id=self.fb_id1,
			                 twitter_id=0,
			                 email="one@mihirmp.com",
			                 date_joined=datetime.now(),
			                 distance_sensitivity=1)

		self.testUser2 = User(fname="Automated2",
			                 lname="Tester2",
			                 fb_id=self.fb_id2,
			                 twitter_id=0,
			                 email="two@mihirmp.com",
			                 date_joined=datetime.now(),
			                 distance_sensitivity=1)
		self.testUser1.save()
		self.testUser2.save()

		u1 = User.objects.get(fb_id=self.fb_id1)
		u2 = User.objects.get(fb_id=self.fb_id2)

		self.id_1 = u1.u_id
		self.id_2 = u2.u_id

		self.hashed_key = follow_hash(self.id_1, self.id_2)

	def testFollowRequest(self):
		u1 = User.objects.get(fb_id=self.fb_id1)
		u2 = User.objects.get(fb_id=self.fb_id2)

		self.id_1 = u1.u_id
		self.id_2 = u2.u_id
		
		follow = c.post('/add_follow/', {'u_id': self.id_1,
			                             'fb_ed': self.fb_id2})


		follow_self = c.post('/add_follow/', {'u_id': self.id_1,
			                                  'fb_ed': self.fb_id1})

		follow_dict = loads(follow.content)
		follow_self_dict = loads(follow_self.content)

		db_follow = get_follow_request(self.id_1, self.id_2)
		db_follow_self = get_follow_request(self.id_1, self.id_1)

		# Can't follow yourself #
		self.assertEquals(db_follow_self['status'], 'error')
		self.assertEquals(follow_self_dict['status'], 'error')

		self.assertEquals(db_follow['status'], 'success')
		self.assertEquals(follow_dict['status'], 'success')
		self.assertEquals(db_follow['req'].follower_p_id, self.id_1)
		self.assertEquals(db_follow['req'].following_p_id, self.id_2)
		self.assertEquals(db_follow['req'].secure_key, self.hashed_key)

	"""def testApproveRequest(self):
		u1 = User.objects.get(fb_id=self.fb_id1)
		u2 = User.objects.get(fb_id=self.fb_id2)

		self.id_1 = u1.u_id
		self.id_2 = u2.u_id

		url = '/approve_request?k=%s&approval=1' % follow_hash(self.id_1, self.id_2)
		print 'url: %s' % url
		print 'id_1: %s, id_2: %s' % (self.id_1, self.id_2)
		approve = c.get(url)
		approve_resp = approve.content

		print "approve_resp: %s" % approve_resp

		db_approve = get_follow_request(self.id_1, self.id_2)

		self.assertEquals(db_approve['status'], "success")
		self.assertEquals(db_approve['req'].approve, 1)"""

