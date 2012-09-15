import hashlib
import smtplib

from json import dumps
from doppio.models import User, FollowPending, Follow, CheckIn
from datetime import datetime
from django.core.mail import send_mail, EmailMessage
from doppio.api.emails import flaggy_email


def __add_user(f_n, l_n, fb, twitter, email):
    try:
        u = User(
            fname=f_n,
            lname=l_n,
            fb_id=fb,
            twitter_id=twitter,
            email=email,
            distance_sensitivity = 1.00,
            date_joined=datetime.now()
            )

        u.save()
        email_info = { }
        email_info["template"] = "welcome"
        email_info["recipient"] = email

        email_res = flaggy_email(email_info)
        msg = email_res['msg']

        if(email_res['status'] == "success"):
            res = success(msg)
            res["u_id"] = str(u.pk)

        elif(email_res['status'] == "error"):
            res = error(msg)

        return res

    except Exception as inst:
        msg = "Unexpected error: %s" % str(inst)
        return error(msg)


def __add_follow(follower, followed_fb, followed_email):
    try:
        f_er = User.objects.get(pk=follower)

        email_info = { }
        email_info["follower"] = f_er.fname
        email_info["recipient"] = followed_email

        if verify_user(followed_fb):
            # Send email to existing user. Add to follow pending table
            f_ed = User.objects.get(fb_id=followed_fb)
            k = hashlib.sha224("%s&%s" % (f_er.pk, f_ed.pk)).hexdigest()
            email_info["key"] = k

            email_info["template"] = "follow"

            mail_status = flaggy_email(email_info)['status']

            if (mail_status == "success"):
                f = FollowPending(follower_p=f_er, following_p=f_ed, secure_key=k)
                f.save()
                res = success("Request sent to %s." % f_ed.fname)
            elif(mail_status == "error"):
                res = error("Failed to send request.")

        else:
            res = error("Facebook user %s not in our database" % followed_fb)

        return res
    
    except User.DoesNotExist:
        return error("Follower Does not exist.")


def __unfollow(follower, followed):
    try:
        f = FollowPending.objects.get(follower_p_id=follower, following_p_id=followed)
        if f.approve:
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

        if req.approve:
            return error("You have already approved this request.")

        else:
            req.approve = True
            f_er = req.follower_p_id
            f_ed = req.following_p_id
            follow = Follow(follower_id=f_er, following_id=f_ed)
            req.save()
            follow.save()
            return success("Request approved!")

    except FollowPending.DoesNotExist:
        return error("No such request!")
    except:
        return error("Error. Could not respond to request.")


def __followers(u_id):
    try:
        array = {}
        for item in Follow.objects.filter(following_id=u_id):
            array[item.follower.pk] = {
                'name': '%s %s' % (item.follower.fname, item.follower.lname),
                'fb_id': item.following.fb_id
                }
        return array

    except User.DoesNotExist:
        return error("Error. User does not exist.")


def __following(u_id):
    try:
        array = {}
        for item in Follow.objects.filter(follower_id=u_id):
            array[item.following.pk] = {
                'name': "%s %s" % (item.following.fname, item.following.lname),
                'fb_id': item.following.fb_id,
                'location': last_check_in(item.following.pk)
                }
        return array

    except User.DoesNotExist:
        return error("Error. User with u_id "+u_id+" does not exist on the Follow table.")


def __check_in(lng, lat, u_id, comm):
    try:
        if comm is None:
            comm = "N/A"

        ci = CheckIn(
            longitude=lng,
            latitude=lat,
            u_id=User.objects.get(pk=u_id),
            when=datetime.now(),
            comment=comm)
        ci.save()

        return success("Checked In!")

    except User.DoesNotExist:
        return error("User with u_id "+str(u_id)+" does not exist.")

    except Exception as inst:
        msg = "Error. Failed to check in: "+str(inst)
        return error(msg)


def __approved_request():
    res = success("Found all approved requests.")
    f = FollowPending.objects.filter(approve=True)
    req_res = { }

    for item in f:
        data = { }

        u = User.objects.get(u_id=int(item.follower_p_id))

        data["p_id"] = int(item.p_id)
        data["follower_p_id"] = int(item.follower_p_id)
        data["follower_name"] = str(u.fname)+" "+str(u.lname)
        data["following_p_id"] = int(item.following_p_id)
        data["secure_key"] = str(item.secure_key)
        data["approve"] = str(item.approve)

        req_res[int(item.p_id)] = data

    res["approved"] = req_res

    return res

def __retrieve_f_request(follower_id, following_id):
    try:
        f = FollowPending.objects.get(follower_p_id=follower_id, following_p_id=following_id)
        res = success("Found request.")
        f_dict = { }
        f_dict["p_id"] = int(f.p_id)
        f_dict["follower_p_id"] = int(f.follower_p_id)
        f_dict["following_p_id"] = int(f.following_p_id)
        f_dict["secure_key"] = str(f.secure_key)
        f_dict["approve"] = str(f.approve)

        res["request"] = f_dict

        return res

    except FollowPending.DoesNotExist:
        return error("Such a follow request does not exist.")

def __unapproved_requests():
    res = success("Found all unapproved requests.")
    f = FollowPending.objects.filter(approve=None)
    req_res = { }

    for item in f:
        data = { }

        u = User.objects.get(u_id=int(item.follower_p_id))

        data["p_id"] = int(item.p_id)
        data["follower_p_id"] = int(item.follower_p_id)
        data["follower_name"] = str(u.fname)+" "+str(u.lname)
        data["following_p_id"] = int(item.following_p_id)
        data["secure_key"] = str(item.secure_key)
        data["approve"] = str(item.approve)

        req_res[int(item.p_id)] = data

    res["unapproved"] = req_res

    return res



## RESPONSES ##

def success(msg):
    return {'status': 'success', 'msg': msg}


def error(msg):
    return {'status': 'error', 'msg': msg}


## HELPERS ##
## Here will be the functions that are not directly mapped to a view ##

def empty_str(s):
    return s == "" or s is None


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
        checkin = CheckIn.objects.filter(u_id=user_id).latest('when')
        return {
            'lng': str(checkin.longitude),
            'lat': str(checkin.latitude),
            'when': str(checkin.when),
            'comment': str(checkin.comment)
        }
    except CheckIn.DoesNotExist:
        return None

#def all_following_info(user_id):
#    try:
#        f = Follow.objects.filter(follower_id=user_id)
