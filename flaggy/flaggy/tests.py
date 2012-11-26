"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils import unittest
from django.test import TestCase
from django.test.client import Client
from doppio.api.controllers import __add_user, __add_follow, __unfollow, __approve_request, __followers, __following, __check_in, __retrieve_f_request, __approved_requests, __nearby, __show_checkins, __update_sensitivity, __pending_request, __poke, __get_sensitivity, __add_incognito
from random import random
from datetime import datetime

class SimpleTest(TestCase):
    def test_basic_addition(self):
    	response = c.get('add_user/?fname=Ilter&lname=Canberk&email=facebook@icanberk.com&fb_id=742077703')
    	self.assertEqual(response.status_code, 200)
    	print response.context['status']
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 3)

"""class ControllerAddUserTestCase(TestCase):
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
		__add_user("Automated", "Tester", self.fb_id, 0, "me@mihirmp.com")
		u = User.objects.get(fb_id=self.fb_id)
		self.assertEquals(u.fname, self.testUser.fname)
		self.assertEquals(u.lname, self.testUser.lname)
		self.assertEquals(u.email, self.testUser.email)


class ControllerAddFollowTestCase(TestCase):
	def setUp(self):
		self.testUser1 = User(fname="Mr",
			                 lname="Smith",
			                 fb_id=int(random()*100000000),
			                 twitter_id=0,
			                 email="mrsmith@mihirmp.com",
			                 date_joined=datetime.now(),
			                 distance_sensitivity=1)"""