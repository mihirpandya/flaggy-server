import hashlib
import datetime
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
        res = success("Found follow request")
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
    try:
        f = Follow.objects.get(follower_id=f_er, following_id=f_ed)
        msg = "Request by %s already approved." % get_pk_user(f_er)['user'].fname
        return success(msg)
    except Follow.DoesNotExist:
        follow = Follow(follower_id=f_er, following_id=f_ed)
        req.save()
        follow.save()
        msg = "You are now connected with %s." % get_pk_user(f_er)['user'].fname
        return success(msg)
    except Exception as inst:
        return error("Error. Please report.")

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

def get_incognito_location(u_id):
    try:
        obj = IncognitoLocation.objects.get(u_id_id=u_id)
        return {
            'lng': str(obj.longitude),
            'lat': str(obj.latitude),
            'when': str(obj.when)
        }
    except IncognitoLocation.DoesNotExist:
        return None

def last_poke(poke_er, poke_ed):
    try:
        poke_er_obj = get_pk_user(poke_er)['user']
        poke_ed_obj = get_pk_user(poke_ed)['user']
        poke = Poke.objects.filter(poke_er=poke_er_obj, poke_ed=poke_ed_obj).latest('when')
        return poke.when

    except Poke.DoesNotExist:
        return datetime.datetime.fromordinal(1)+datetime.timedelta(seconds=5*3600);

## Auth ##

def store_token(u_id, token, device):
    try:
        u = UserTokens.objects.get(u_id_id=u_id, device=device)
        u.token = token
        u.save()
    except UserTokens.DoesNotExist:
        tok_u = UserTokens(u_id_id=u_id, token=token, device=device)
        tok_u.save()

# default action is to return token of iPhone #
def get_token(u_id, device):
    print "u_id: %s, device: %s" % (u_id, device)
    if device is None:
        try:
            tok = UserTokens.objects.get(u_id_id=int(u_id), device="iPhone").token
            return tok
        except Exception as inst:
            return None
    else: 
        try:
            tok = UserTokens.objects.get(u_id_id=int(u_id), device=device).token
            return tok
        except:
            return None

# takes care of 5 hour offset because of time difference with server #
def server_offset(time):
    d = datetime.timedelta(seconds=5*60*60)
    return time-d

## Time based functions ##
def get_datetime(time_str):
    try:
        parse_this_time = time_str.split(time_str[19])[0]
        print "parse_this_time: %s" % parse_this_time
    except:
        parse_this_time = time_str
    return datetime.datetime.strptime(parse_this_time, '%Y-%m-%d %H:%M:%S')

def too_frequent(curr_time, prev_time, diff_seconds):
    prev = server_offset(get_datetime(prev_time))
    curr = get_datetime(curr_time)
    diff = curr-prev

    print "days: %s, seconds: %s" % (diff.days, diff.seconds) # offset of 5 hours from server
    print "prev: %s" % prev
    print "curr: %s" % curr

    if(diff.seconds >= diff_seconds):
        print "not too frequent"
        return False
    
    return True
