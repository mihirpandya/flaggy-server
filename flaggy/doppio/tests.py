"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils import unittest
from django.test import TestCase
from django.test.client import Client
from doppio.models import *
from doppio.api.controllers import __add_user as c_add_user
from doppio.api.controllers import __add_follow as c_add_follow
from doppio.api.utils import follow_hash
from random import random
from datetime import datetime

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

	def testAddUser(self):
		c_add_user("Automated", "Tester", self.fb_id, 0, "me@mihirmp.com")
		u = User.objects.get(fb_id=self.fb_id)
		self.assertEquals(u.fname, self.testUser.fname)
		self.assertEquals(u.lname, self.testUser.lname)
		self.assertEquals(u.email, self.testUser.email)

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
		self.id_1 = self.testUser1.u_id
		self.id_2 = self.testUser2.u_id
		self.hash = follow_hash(self.id_1, self.id_2)

	def testFollowRequest(self):
		c_add_follow(self.id_1, self.fb_id2)
		try:
			u = FollowPending.objects.get(follower_p_id=self.id_1, following_p_id=self.id_2)
			self.assertEquals(u.hash, self.hash)
			self.assertEquals(u.approve, None)
		except:
			False