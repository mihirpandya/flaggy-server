from notifications.push import send_push
from json import dumps
from doppio.api.utils import *
from doppio.api.proximity import coord_dict, too_close, close_enough, coord_distance
from doppio.api.responses import success, error, is_Success, is_Error, get_Msg

def check_in_payload(u_id, fname, lng, lat, time):
    result = { }
    result['aps'] = { }
    result['aps']['alert'] = "%s just checked in near you." % fname
    result['aps']['sound'] = 'default'
    result['data'] = { }
    result['data']['u_id'] = u_id
    result['data']['lng'] = str(lng)
    result['data']['lat'] = str(lat)
    result['data']['time'] = time

    return result

def add_follow_payload(follower_name):
    result = { }
    result['aps'] = { }
    result['aps']['alert'] = "%s wants to follow you!" % follower_name
    result['aps']['sound'] = 'default'

    return result

def accepted_payload(following_name):
    result = { }
    result['aps'] = { }
    result['aps']['alert'] = "%s accepted your request!" % following_name
    result['aps']['sound'] = 'default'

    return result


def poke_payload(name):
    result = { }
    result['aps'] = { }
    result['aps']['alert'] = "%s wants to know where you are!" % name
    result['aps']['sound'] = 'default'

    return result


def safe_distance(follower_id, loc_obj):
    sensitivity = get_sensitivity(follower_id)
    prev_checkin_full = last_check_in(follower_id)
    if(prev_checkin_full is not None):
        prev_checkin = coord_dict(float(prev_checkin_full['lng']), float(prev_checkin_full['lat']))
        print "In safe_distance. %s, %s, %s" % (follower_id, prev_checkin, loc_obj)
        if close_enough(prev_checkin, loc_obj, sensitivity):
            print "close enough."
            return coord_distance(prev_checkin, loc_obj)
        else:
            return -1
    else:
        return 1

def push_all_followers(u_id, followers_l, loc_obj, payload):
    outcome = True
    user = User.objects.get(pk=u_id)
    fname = user.fname
    for el in followers_l:
        follower_id = el.follower_id
        u = User.objects.get(pk=follower_id)
        follower_token = get_token(u.u_id, None)
        dist = safe_distance(el.follower_id, loc_obj)
        print "dist: %s" % dist
        if (dist > 0):
            notif_status = send_push(str(follower_token), dumps(payload))
            print "%s %s" % (el.follower_id, notif_status['msg'])
            if(is_Error(notif_status)): outcome = outcome and False
    return outcome


# Notifies followers of u_id about the check in
def notify_check_in(u_id, lng, lat, when):
    followers = Follow.objects.filter(following_id=u_id)
    user_checking_in = get_pk_user(u_id)['user']
    u_id_fname = user_checking_in.fname # For payload
    prev_checkin_dict = get_incognito_location(u_id)
    curr_checkin = coord_dict(float(lng), float(lat))

    if(prev_checkin_dict is not None):
        prev_time = prev_checkin_dict['when']
        #offset_prev = prev_time

        if(not too_frequent(when, prev_time, 0)): # 30 seconds since last check in
            payload = check_in_payload(u_id, u_id_fname, curr_checkin['lng'], curr_checkin['lat'], when)
            if push_all_followers(u_id, followers, curr_checkin, payload):
                res = success("Sent push notifications to all followers.")
                res['payload'] = payload
            else:
                res = error("Could not send push notifications to some followers.")

        else:
            res = error("Current check in too soon!")

    else:
        payload = check_in_payload(u_id, u_id_fname, curr_checkin['lng'], curr_checkin['lat'], None)
        if push_all_followers(u_id, followers, curr_checkin, payload):
            res = success("Sent push notifications.")
            res['payload'] = payload
        else:
            res = error("Could not send push notifications to some followers.")

    return res

def notify_add_follow(follower_name, u_id):
    payload = add_follow_payload(follower_name)
    token = get_token(u_id, None)
    notif_status = send_push(str(token), dumps(payload))

    return notif_status


def notify_accepted(u_id, followed_id):
    followed = get_pk_user(followed_id)['user']
    followed_name = "%s %s" % (str(followed.fname), str(followed.lname))
    payload = accepted_payload(followed_name)
    token = get_token(u_id, None)
    notif_status = send_push(str(token), dumps(payload))

    return notif_status

def notify_poke(poke_er, poke_ed):
    user = get_pk_user(poke_ed)['user']
    poked_by = get_pk_user(poke_er)['user']
    poked_by_name = str(poked_by.fname)
    payload = poke_payload(poked_by_name)
    token = get_token(poke_ed, None)
    notif_status = send_push(str(token), dumps(payload))

    return notif_status


