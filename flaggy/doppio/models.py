from django.db import models


class User(models.Model):
    u_id = models.AutoField(primary_key=True)
    fname = models.CharField(max_length=30)
    lname = models.CharField(max_length=30)
    fb_id = models.IntegerField()
    twitter_id = models.IntegerField()
    email = models.EmailField(max_length=100)
    date_joined = models.DateField()
    distance_sensitivity = models.FloatField()
    token = models.CharField(max_length=100)


class CheckIn(models.Model):
    c_id = models.AutoField(primary_key=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    u_id = models.ForeignKey(User)
    when = models.DateTimeField()
    comment = models.TextField()


class Follow(models.Model):
    f_id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(User, related_name='follower')
    following = models.ForeignKey(User, related_name='following')


class FollowPending(models.Model):
    p_id = models.AutoField(primary_key=True)
    follower_p = models.ForeignKey(User, related_name='follower_p')
    following_p = models.ForeignKey(User, related_name='following_p')
    secure_key = models.CharField(max_length=56)
    approve = models.NullBooleanField()
