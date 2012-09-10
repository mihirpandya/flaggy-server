import sys
import pprint
import hashlib
import smtplib

from doppio.models import *
from datetime import datetime
from django.utils import simplejson
from django.core import serializers
from django.core.mail import send_mail


def __add_user(f_n, l_n, fb, twitter, email):
    d = datetime.now()
    try:
        u = User(fname=f_n, lname=l_n, fb_id=fb, twitter_id=twitter, email=email, date_joined=d)
        u.save()
        send_mail("Welcome to Flaggy App!", "Thank you for joining Flaggy App!", 'firepent@hotmail.com', [u.email], fail_silently=False)

        return str(u.pk)

    except:
        return 0

def __add_follow(follower, followed_fb, followed_email):
    try:
        f_er = User.objects.get(pk=follower)

        if(verify_user(followed_fb)):
            # Send email to existing user. Add to follow pending table

            f_ed = User.objects.get(fb_id=followed_fb)
            k = hashlib.sha224(str(f_er.pk)+"&"+str(f_ed.pk)).hexdigest()
            approve_url = "http://flaggy-mihirmp.dotcloud.com/approve_request?k="+k

            try:
                mail_status = send_mail(f_er.fname+" wants to follow you on Flaggy App!", approve_url, 'notification@flaggyapp.com', [followed_email], fail_silently=False)

                if(mail_status):
                    f = FollowPending(follower_p=f_er, following_p=f_ed, secure_key=k)
                    f.save()
                    res = success("Request sent to "+f_ed.fname+".")

                else:
                    res = error("Failed to send request.")

            except smtplib.SMTPException:
                res = error("Failed to send request. SMTP server disconnected unexpectedly.")

        else:
            # Send email about flaggy and follow request.
            try:
                mail_status = send_mail(f_er.fname+" wants to follow you on Flaggy App!", f_er.fname+" wants you to join Flaggy.", 'notification@flaggyapp.com', [followed_email], fail_silently=False)
                if(mail_status):
                    res = success("New friend notified about flaggy.")
                else:
                    res = error("Failed to notify about flaggy.")

            except smtplib.SMTPException:
                res = error("Failed to notify about flaggy. SMTP server disconnected unexpectedly.")

        return res
    
    except User.DoesNotExist:
        return error("Follower Does not exist.")


def __unfollow(follower, followed):
    try:
        f = FollowPending.objects.get(follower_p_id=follower, following_p_id=followed)
        
        if(f.approve):
            f.approve = False
            follow = Follow.objects.get(follower_id=follower, following_id=followed)

            f.delete()
            follow.delete()

            return success("Successfully unfollowed.")
        
        else:
            return error("Already unfollowed.")

    except FollowPending.DoesNotExist:
        return error("No such connection exists.")
    except:
        return error("Error. Could not unfollow.")


def __approve_request(k):
    try:
        req = FollowPending.objects.get(secure_key=k)

        if(req.approve):
            return error("You have already approved this request.")

        else:
            req.approve = True
            f_er = req.follower_p_id
            f_ed = req.following_p_id
            follow = Follow(follower_id = f_er, following_id = f_ed)

            req.save()
            follow.save()

            return success("Request approved!")

    except FollowPending.DoesNotExist:
        return error("No such request!")
    except:
        return error("Error. Could not respond to request.")

def __followers(u_id):

    try:
        follower_list = Follow.objects.filter(following_id=u_id)
        array = { }
        for item in follower_list:
            dict_user = { }
            dict_user['name'] = item.follower.fname + " " + item.follower.lname
            array[item.follower.pk] = dict_user

        return array

    except User.DoesNotExist:
        return error("Error. User does not exist.")

def __following(u_id):
    try: 
        following_list = Follow.objects.filter(follower_id=u_id)
        print following_list
        array = { }
        for item in following_list:
            dict_user = { }
            ##dict_user['u_id'] = item.following.pk
            dict_user['name'] = item.following.fname + " " + item.following.lname
            dict_user['location'] = last_check_in(item.following.pk)
            array[item.following.pk] = dict_user

        return array

    except User.DoesNotExist:
        return error("Error. User does not exist.")

def __check_in(long, lat, u_id, comm):
    d = datetime.now()
    
    try:
        user = User.objects.get(pk=u_id)
        if (comm is None):
            comm = "N/A"
        
        ci = CheckIn(longitude = long,
                     latitude = lat,
                     u_id = user,
                     when = d,
                    comment = comm)
        ci.save()

        return success("Checked In!")
    
    except:
        return error("Error. Failed to check in.")

## RESPONSES ##

def success(msg):
    success = { }
    success["status"] = "success"
    success["msg"] = msg

    return success

def error(msg):
    error = { }
    error["status"] = "error"
    error["msg"] = msg

    return error

## HELPERS ##
## Here will be the functions that are not directly mapped to a view ##
def empty_str(s):
    return (s == "" or s is None)

def verify_user(value):
    try:
        User.objects.get(fb_id=value)
        return True
    except User.MultipleObjectsReturned:
        return True
    except User.DoesNotExist:
        return False

def last_check_in(user_id):
    try:
        checkin = CheckIn.objects.filter(u_id = user_id).latest('when')
        coor = { }
        coor["long"] = str(checkin.longitude)
        coor["lat"] = str(checkin.latitude)
        coor["when"] = str(checkin.when)
        coor["comment"] = str(checkin.comment)

        return coor
    except CheckIn.DoesNotExist:
        return None

#def all_following_info(user_id):
#    try:
#        f = Follow.objects.filter(follower_id=user_id)



