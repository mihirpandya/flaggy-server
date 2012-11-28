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
from random import random
from datetime import datetime

class ControllerAddUserTestCase(unittest.TestCase):
	def setUp(self):
		self.fb_id = int(random()*100000000)
		self.testUser = User(fname="Automated",
			                 lname="Tester",
			                 fb_id=int(random()*100000000),
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