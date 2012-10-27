import hashlib
from doppio.models import *
from doppio.api.responses import success, error, is_Error, is_Success, get_Msg

## MODELS RELATED METHODS ##
### Here will be the functions that complete specific model-related tasks ###

def get_pk_user(pk):
    try:
        user = User.objects.get(u_id=pk)
        res = success('Found user.')
        res['user'] = user

        return res
    except Exception as inst:
        return error("Error: %s " % inst)

def get_fb_user(fb_id):
    try:
        user = User.objects.get(fb_id=fb_id)
        res = success('Found FB user.')
        res['user'] = user

        return res
    except Exception as inst:
        return error("Error: %s " %inst)

def get_follow_request(f_er, f_ing):
    try:
        req = FollowPending.objects.get(follower_p_id=f_er, following_p_id=f_ing)
        res = success()
        res['req'] = req

        return res

    except Exception as inst:
        return error("Error: %s " % inst)

def get_follow(f_er, f_ing):
    try:
        follow = Follow.objects.get(follower_id=follower, following_id=followed)
        res = success()
        res['follow'] = follow

        return res
    except Exception as inst:
        return error("Error: %s " % inst)

def get_sensitivity(u_id):
    u = User.objects.get(u_id=u_id)
    return u.distance_sensitivity


def follow_hash(u_id1, u_id2):
    return hashlib.sha224("%s&%s" % (u_id1, u_id2)).hexdigest()

def follow_exists(k):
    fp = FollowPending.objects.filter(secure_key=k)
    return (len(fp) >= 1)

## Requests ##

# Adds to Follow table and sends notification to person who added #
def accept(req):
    req.approve = True
    f_er = req.follower_p_id
    f_ed = req.following_p_id
    follow = Follow(follower_id=f_er, following_id=f_ed)
    req.save()
    follow.save()
    notify_accepted(f_ed)
    return success("Request approved!")

def reject(req):
    req.approve = False
    f_er = req.follower_p_id
    f_ed = req.following_p_id
    req.save()
    return success("Request rejected.")

def empty_str(s):
    return s == "" or s is None

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

## Auth ##

def store_token(u_id, token):
    u = User.objects.get(u_id=u_id)
    u.token=token
    u.save()

def get_token(u_id):
    u = User.objects.get(u_id=u_id)
    return u.token
