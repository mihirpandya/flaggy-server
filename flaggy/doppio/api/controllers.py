import hashlib
import smtplib
from json import dumps
from datetime import datetime
from django.core.mail import send_mail, EmailMessage
from doppio.models import User, FollowPending, Follow, CheckIn, IncognitoLocation
from doppio.api.emails import flaggy_email
from doppio.api.proximity import coord_distance
from doppio.api.notify import check_in_payload, push_all_followers, notify_check_in, notify_add_follow, notify_accepted, notify_poke
from doppio.api.responses import success, error, is_Success, is_Error, get_Msg
from doppio.api.utils import *

## HELPERS ##
## Here will be the functions that are not directly mapped to a view ##


## REQUEST HANDLERS ##

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

        ## Email welcome message to new user ##
        email_info = { }
        email_info["template"] = "welcome"
        email_info["recipient"] = email
        email_res = flaggy_email(email_info)

        msg = get_Msg(email_res)

        if(is_Success(email_res)):
            res = success(msg)
            res["u_id"] = str(u.pk)

        elif(is_Error(email_res)):
            res = error(msg)

        return res

    except Exception as inst:
        msg = "Unexpected error: %s" % str(inst)
        return error(msg)

## FOLLOW AND UNFOLLOW ##

def __add_follow(follower_id, followed_fb):
    follower = get_pk_user(follower_id)
    followed = get_fb_user(followed_fb)
    print follower
    print followed

    if(is_Error(follower)): res = follower

    elif(is_Success(follower)):
        f_er = follower['user']
        # Disallow users to follow themselves! #
        if(int(f_er.fb_id) == int(followed_fb)):
            return error("Why do you want to follow yourself?")

        email_info = { }
        email_info["follower"] = f_er.fname

        if(is_Error(followed)):
            res = error("Facebook user %s not in our database" % followed_fb)

        elif(is_Success(followed)):
            # Send email to existing user. Add to follow pending table
            f_ed = followed['user']

            k = follow_hash(f_er.pk, f_ed.pk)

            if(not follow_exists(k)):
                email_info["key"] = k
                email_info["template"] = "follow"
                email_info["recipient"] = f_ed.email

                mail_status = flaggy_email(email_info)
                full_name = str(f_er.fname) + " " + str(f_er.lname)
                notif_status = notify_add_follow(full_name, f_ed.u_id)
                #add_follow_notify

                if (is_Success(mail_status)):
                    f = FollowPending(follower_p=f_er, following_p=f_ed, secure_key=k)
                    f.save()
                
                    res = success("Request sent to %s." % f_ed.fname)

                elif(is_Error(mail_status)):
                    res = error("Failed to send email request.")
            else:
                res = success("Request has already been sent.")

    return res


def __unfollow(follower, followed):
    req = get_follow_request(follower, followed)
    follow = get_follow(follower, followed)

    if(is_Error(req)): res = req

    elif(is_Success(req)):

        f = req['req']

        if (f.approve and is_Success(follow)):
            f.approve = False
            curr_follow = follow['follow']
            f.delete()
            curr_follow.delete()
            res =success("Successfully unfollowed.")
        else:
            res = error("Already unfollowed.")
    return res

def __approve_request(k, approval):
    try:
        req = FollowPending.objects.get(secure_key=k)

        if(approval == 1): 
            notify_accepted(req.follower_p_id, req.following_p_id)
            return accept(req)    
        elif(approval == 0): return reject(req)        
        else: return error("Invalid approval handle.")

    except FollowPending.DoesNotExist: return error("No such request!")
    except Exception as inst:
        return error("Error. Could not respond to request. Exception %s" % inst)


def __followers(u_id):
    try:
        array = {}
        res = success("Obtained all followers.")
        for item in Follow.objects.filter(following_id=u_id):
            array[item.follower.pk] = {
                'name': '%s %s' % (item.follower.fname, item.follower.lname),
                'fb_id': item.follower.fb_id,
                'u_id': item.follower.pk,
                'location': last_check_in(item.follower.pk)
                }
        res['followers'] = array
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
                'u_id': item.following.pk,
                'location': last_check_in(item.following.pk)
                }
        return array

    except User.DoesNotExist:
        return error("Error. User with u_id "+u_id+" does not exist on the Follow table.")

def __approved_requests():
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
    f = get_follow_request(follower_id, following_id)

    if(f['status'] == "error"): res = f

    elif(f['status'] == "success"):
        res = success("Found request.")
        f_dict = { }
        f_dict["p_id"] = int(f.p_id)
        f_dict["follower_p_id"] = int(f.follower_p_id)
        f_dict["following_p_id"] = int(f.following_p_id)
        f_dict["secure_key"] = str(f.secure_key)
        f_dict["approve"] = str(f.approve)

        res["request"] = f_dict

    return error("Such a follow request does not exist.")

def __pending_request(u_id):
    f = FollowPending.objects.filter(following_p_id=u_id, approve=None)
    req_res = [ ]
    for item in f:
        data= { }
        u = User.objects.get(u_id=int(item.follower_p_id))

        data["p_id"] = int(item.p_id)
        data["follower_p_id"] = int(item.follower_p_id)
        data["follower_name"] = str(u.fname)+" "+str(u.lname)
        data["following_p_id"] = int(item.following_p_id)
        data["secure_key"] = str(item.secure_key)
        data["approve"] = str(item.approve)

        req_res.append(data)
    return req_res


## CHECKING IN ##

def __check_in(lng, lat, u_id, comm):
    try:
        if comm is None:
            comm = "N/A"

        when = datetime.datetime.now()
        notif = notify_check_in(u_id, lng, lat, str(when))
        ci = CheckIn(
            longitude=lng,
            latitude=lat,
            u_id=User.objects.get(pk=u_id),
            when=when,
            comment=comm)
        ci.save()

        if(is_Success(notif)):
            print 'success!'
            res = success("Checked In! %s" % notif['msg'])
            res['payload'] = notif['payload']
            return res

        elif(is_Error(notif)):
            return error("Checked in but %s" % notif['msg'])

    except User.DoesNotExist:
        return error("User with u_id "+str(u_id)+" does not exist.")

#    except Exception as inst:
#        msg = "Error. Failed to check in: %s " % inst
#        return error(msg)

def __show_checkins(u_id):
    checkins = CheckIn.objects.filter(u_id_id=u_id)

    result = { }

    i = 0

    for curr in checkins:
        c = { }
        c['lat'] = int(curr.latitude)
        c['lng'] = int(curr.longitude)
        c['when'] = str(curr.when)
        c['comm'] = str(curr.comment)
        c['c_id'] = int(curr.c_id)

        result[i] = c
        i+=1
    res = success("Found all check ins.")
    res['checkins'] = result

    return res

def __nearby(u_id):
    if(get_pk_user(u_id) is None):
        return error("User %s does not exist" % u_id)
    else:
        user = User.objects.get(pk=u_id)
        coord = last_check_in(u_id)
        lat = coord['lat']
        lng = coord['lng']
        proximity = user.distance_sensitivity

        followers = __followers(u_id)

        if(followers != None):
            all_followers = [ ]

            for item in followers.keys():
                coord = { }
                coord['key'] = item
                try:
                    coord['lat'] = followers[item]['location']['lat']
                    coord['lng'] = followers[item]['location']['lng']
                    all_followers.append(coord)
                except:
                    all_followers.append(coord)

            user_obj = { }
            user_obj['lat'] = float(lat)
            user_obj['lng'] = float(lng)

#            print all_followers

            nearby_followers = [ ]

            for item in all_followers:
                try:
                    curr_obj = { }
                    curr_obj['lat'] = float(item['lat'])
                    curr_obj['lng'] = float(item['lng'])

                    if(coord_distance(user_obj, curr_obj) < proximity):
                        nearby_followers.append(item)

                except Exception as inst:
                    curr_obj = {}

            res = success("Returning last check ins of all followers")
            res['followers'] = nearby_followers
            return res

        else:
            res = success("No followers.")
            res['followers'] = [ ]
            return res

def __update_sensitivity(u_id, sensitivity):
    user_obj = get_pk_user(u_id)
    if is_Success(user_obj): 
        user = user_obj['user']
        user.distance_sensitivity = sensitivity
        user.save()
        return success("Sensitivity updated to %s" % sensitivity)
    elif is_Error(user_obj):
        return error("No user with u_id %s" % u_id)

def __get_sensitivity(u_id):
    user_resp = get_pk_user(u_id)
    if is_Error(user_resp): return user_resp
    else:
        res = success("Found sensitivity")
        res["sensitivity"] = user_resp['user'].distance_sensitivity

        return res

def __poke(poke_er, poke_ed):
    try:
        prev_poke = last_poke(poke_er, poke_ed)-datetime.timedelta(0, 3600*5)
        now = datetime.datetime.now()

        if(prev_poke is not None):
            print "wtf %s" % prev_poke
            if(too_frequent(str(now), str(prev_poke), 30)): # 2 minutes before next poke
                return error("Poking too soon!")

        poke_er_user = get_pk_user(poke_er)['user']
        poke_ed_user = get_pk_user(poke_ed)['user']
        poke_model = Poke(poke_er=poke_er_user, poke_ed=poke_ed_user, when=now)
        poke_model.save()
        notify_poke(poke_er, poke_ed)

        return success("Poked and notified!")
    except Exception as inst:
        return error("Error poking. %s" % inst)

def __add_incognito(u_id, lng, lat):
    try:
        i_obj = IncognitoLocation.objects.get(u_id_id=u_id)
        i_obj.lng = lng
        i_obj.lat = lat
        i_obj.save()

        return success("Updated user %s's location" % u_id)

    except IncognitoLocation.DoesNotExist:
        i_obj = IncognitoLocation(u_id_id=u_id, longitude=lng, latitude=lat)
        i_obj.save()

        return success("Saved new entry of user %s" % u_id)

    except Exception as inst:
        return error("Error. %s" % inst)






