from doppio.push import send_push
from doppio.api.proximity import coord_dict, comfortable_range
from doppio.api.responses import success, error, is_Success, is_Error, get_Msg

def check_in_payload(fname, lng, lat):
    result = { }
    result['aps'] = { }
    result['aps']['alert'] = "%s just checked in at %s, %s" % (fname, lng, lat)
    result['aps']['sound'] = 'default'
    result['data'] = { }
    result['data']['u_id'] = u_id
    result['data']['lng'] = str(lng)
    result['data']['lat'] = str(lat)

    return result

def push_all_followers(followers_l, payload):
    outcome = True
    print "Entered!"
    for el in followers_l:
        follower_id = el.follower_id
        u = User.objects.get(pk=follower_id)
        follower_token = u.token
        notif_status = send_push(str(follower_token), dumps(payload))
#        print "%s %s" % (el.follower_id, notif_status['msg'])
        if(is_Error(notif_status)): outcome = outcome and False
    return outcome

# Notifies followers of u_id about the check in
def notify_check_in(u_id, lng, lat):
    followers = Follow.objects.filter(following_id=u_id)
    user_checking_in = get_pk_user(u_id)['user']
    u_id_fname = user_checking_in.fname # For payload
    payload = check_in_payload(str(u_id_fname), str(lng), str(lat))
    prev_checkin_dict = last_check_in(u_id)
    curr_checkin = coord_dict(float(lng), float(lat))

    if(prev_checkin_dict is not None):
        prev_checkin = coord_dict(float(prev_checkin_dict['lng']), float(prev_checkin_dict['lat']))

#        if(comfortable_range(prev_checkin, curr_checkin, 0.0)):
        if push_all_followers(followers, payload):
            res = success("Sent push notifications to all followers.")
        else:
            res = error("Could not send push notifications to some followers.")

#        else:
#            res = error("Current check in is not in comfortable range.")

    else:
        if push_all_followers(followers, payload):
            print "I was here!"
            res = success("Sent push notifications.")
        else:
            res = error("Could not send push notifications to some followers.")

    return res
