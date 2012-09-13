"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils import unittest
from django.test import TestCase
from django.test.client import Client

class SimpleTest(TestCase):
    def test_basic_addition(self):
    	response = c.get('add_user/?fname=Ilter&lname=Canberk&email=facebook@icanberk.com&fb_id=742077703')
    	self.assertEqual(response.status_code, 200)
    	print response.context['status']
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 3)
