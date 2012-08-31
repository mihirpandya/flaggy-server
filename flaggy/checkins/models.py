from django.db import models

class User(models.Model):
	u_id = models.AutoField(primary_key=True)
	fname = models.CharField(max_length=30)
	lname = models.CharField(max_length=30)
	fb_id = models.IntegerField()
	twitter_id = models.IntegerField()
	email = models.EmailField(max_length=100)
	date_joined = mails.DateField()

class CheckIn(models.Model):
	c_id = models.AutoField(primary_key=True)
	longitude = models.DecimalField(max_digits = 10, decimal_places=9)
	latitude = models.DecimalField(max_digits = 10, decimal_places=9)
	u_id = models.ForeignKey(User)
	when = models.DateField()
	comment = models.TextField()

class Follow(models.Model):
	f_id = models.AutoField(primary_key=True)
	follower = models.ForeignKey(User, related_name='follower')
	following = models.ForeignKey(User, related_name='following')
