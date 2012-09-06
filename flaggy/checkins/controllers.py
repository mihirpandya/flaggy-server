import sys
import pprint
import hashlib
import smtplib

from checkins.models import User, CheckIn, Follow, FollowPending
from datetime import datetime
from django.utils import simplejson
from django.core import serializers
from django.core.mail import send_mail


def verify_user(value):
    try:
        User.objects.get(fb_id=value)
        return True
    except User.MultipleObjectsReturned:
        return True
    except User.DoesNotExist:
        return False

def __add_user(f_n, l_n, fb, twitter, email):
    d = datetime.now()
    try:
        u = User(fname=f_n, lname=l_n, fb_id=fb, twitter_id=twitter, email=email, date_joined=d)
        u.save()
        send_mail("Welcome to Flaggy App!", "Thank you for joining Flaggy App!", 'firepent@hotmail.com', [u.email], fail_silently=False)

        return str(u.pk)

    except:
        return "Error. User could not be created. Problem with __add_user."

def __add_follow(follower, followed):
    try:
        f_er = User.objects.get(pk=follower)
        f_ed = User.objects.get(pk=followed)
        k = hashlib.sha224(str(f_er.pk)+"&"+str(f_ed.pk)).hexdigest()

    except User.DoesNotExist:
        return "User does not exist."

    except FollowPending.MultipleObjectsReturned:
        return "Request to "+f_ed.fname+" has already been sent."

    except:
        return "Error. Could not send follow request to "+f_ed.fname


    try:
        FollowPending.objects.get(secure_key=k)
        return "Request to "+f_ed.fname+" has already been sent."

    except FollowPending.DoesNotExist:
        approve_url = "http://flaggy-mihirmp.dotcloud.com/approve_request?k="+k

        try:
            mail_success = send_mail(f_er.fname+" wants to follow you on Flaggy App!", approve_url, 'firepent@hotmail.com', [f_ed.email], fail_silently=False)

            if(mail_success):
                f = FollowPending(follower_p=f_er, following_p=f_ed, secure_key=k)
                f.save()
                res = "Request sent to "+f_ed.fname
            else:
                res = "Failed to send request "+f_ed.fname

            return res

        except User.DoesNotExist:
        #smtplib.SMTPException:
            return "SMTP Server Disconnected unexpectedly."


def __unfollow(follower, followed):
    try:
        f = FollowPending.objects.get(follower_p_id=follower, following_p_id=followed)
        
        if(f.approve):
            f.approve = False
            follow = Follow.objects.get(follower_id=follower, following_id=followed)

            f.save()
            follow.delete()

            return "Successfully unfollowed."
        
        else:
            return "Already unfollowed."

    except FollowPending.DoesNotExist:
        return "No such connection exists."
    except:
        return "Error. Could not unfollow."


def __approve_request(k):
    try:
        req = FollowPending.objects.get(secure_key=k)

        if(req.approve):
            return "You have already approved this request."

        else:
            req.approve = True
            f_er = req.follower_p_id
            f_ed = req.following_p_id
            follow = Follow(follower_id = f_er, following_id = f_ed)

            req.save()
            follow.save()

            return "Request approved!"

    except FollowPending.DoesNotExist:
        return "No such request!"
    except:
        return "Error. Could not respond to request."

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
        return "Error. User does not exist."

def __following(u_id):
    try: 
        following_list = Follow.objects.filter(follower_id=u_id)
        print following_list
        array = { }
        for item in following_list:
            dict_user = { }
            ##dict_user['u_id'] = item.following.pk
            dict_user['name'] = item.following.fname + " " + item.following.lname
            dict_user['location'] = last_check_in(item.follower.pk)
            array[item.following.pk] = dict_user

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

#def all_following_info(user_id):
#    try:
#        f = Follow.objects.filter(follower_id=user_id)



