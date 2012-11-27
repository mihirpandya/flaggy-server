from doppio.models import User, CheckIn, Follow, FollowPending
from doppio.api.controllers import __add_user, __add_follow, __unfollow, __approve_request, __followers, __following, __check_in, __retrieve_f_request, __approved_requests, __nearby, __show_checkins, __update_sensitivity, __pending_request, __poke, __get_sensitivity, __add_incognito
from doppio.api.twilio import sendSMS
from json import dumps
from django.template import Context, loader
from datetime import datetime
from django.http import HttpResponse
from notifications.push import send_push
from doppio.api.responses import success, error, is_Success, is_Error, get_Msg
from doppio.api.utils import *

def add_user(request):
    if request.method == 'POST':
        f_n = request.POST.get('fname')
        l_n = request.POST.get('lname')
        fb_id = request.POST.get('fb_id')
        email = request.POST.get('email')
        tok = request.POST.get('tok')
        device = request.POST.get('device')
        res = { }
        checkin_user = { }

        if(is_Success(get_fb_user(fb_id))):
            u = User.objects.get(fb_id=fb_id)
            last_checkin = last_check_in(u.u_id)

            if last_checkin is not None: checkin_user = last_checkin

            res["status"] = 2
            res["msg"] = "User "+u.fname+" already exists!"
            res["last_checkin"] = checkin_user
            res["u_id"] = str(u.u_id)
            res["following"] = __following(u.u_id)
            res["follower"] = __followers(u.u_id)

        elif not empty_str(f_n) and not empty_str(l_n) and not empty_str(fb_id):
            add_status = __add_user(f_n, l_n, fb_id, 0000, email)
            u = User.objects.get(fb_id=db_id)
            #store_token(u.u_id, token, device)
            
            if(is_Success(add_status)):
                res["status"] = 1
                res["msg"] = add_status["msg"]
                res["u_id"] = add_status["u_id"]
                res["last_checkin"] = None
                res["following"] = None

            else:
                res["status"] = 0
                res["msg"] = add_status["msg"]
        else:
            res["status"] = 0
            res["msg"] = "Invalid input."

        return HttpResponse(dumps(res), mimetype='application/json')

    else:
        return HttpResponse(dumps(error("No POST request received.")), mimetype='application/json')


def add_token(request):
    if request.method == 'POST':
        u_id = request.POST.get('u_id')
        device = request.POST.get('device')
        tok = request.POST.get('tok')

        store_token(u_id, tok, device)

        return HttpResponse(dumps(success("Added token")), mimetype='application/json')
    else:
        return HttpResponse(dumps(error("No POST request received.")), mimetype='application/json')        

## Methods related to following. ##
def add_follow(request):
    if request.method == 'POST':
        follower = request.POST.get('u_id')
        followed_fb = request.POST.get('fb_ed')

        if follower is not None and followed_fb is not None:
            if(is_Success(get_fb_user(followed_fb))):
                u = User.objects.get(fb_id=followed_fb)
                res = __add_follow(follower, followed_fb)
                return HttpResponse(dumps(res), mimetype='application/json')

            else:
                resp = success("Facebook user %s is not on our database." % followed_fb)
                return HttpResponse(dumps(resp), mimetype='application/json')

        elif followed_fb is None:
            err = error("Facebook ID of the person you want to follow is missing.")
            return HttpResponse(dumps(err), mimetype='application/json')

    else:
        err = error("No request received.")
        return HttpResponse(dumps(err), mimetype='application/json')


def approve_request(request):
    if request.method == 'GET':
        key = request.GET.get('k')
        approval = request.GET.get('approval')
        if (approval is not None and key is not None):
            res = __approve_request(key, int(approval))
            return HttpResponse(dumps(res), mimetype='application/json')
        else:
            return HttpResponse(dumps(error("Invalid input.")), mimetype='application/json')


def unfollow(request):
    if request.method == 'POST':
        f_er = request.POST.get('f_er')
        f_ed = request.POST.get('f_ed')
        res = __unfollow(f_er, f_ed)
        return HttpResponse(dumps(res), mimetype='application/json')


def followers(request):
    if request.method == 'POST':
        u_id = request.POST.get('u_id')
        res = __followers(u_id)
        if is_Success(res):
            result = success("Retrieved followers.")
            result['followers'] = res['followers']
        elif is_Error(res):
            result = error(res['msg'])

        return HttpResponse(dumps(result), mimetype='application/json')

    else:
        err = error("No request received.")
        return HttpResponse(dumps(err), mimetype='application/json')


def following(request):
    if request.method == 'POST':
        u_id = request.POST.get('u_id')
        res = __following(u_id)
        result = success("Retrieved people you are following.")
        result['following'] = res
        return HttpResponse(dumps(result), mimetype='application/json')

    else:
        err = error("No request received.")
        return HttpResponse(dumps(err), mimetype='application/json')

def approved_requests(request):
    if request.method == 'POST':
        res = __approved_request()
        return HttpResponse(dumps(res), mimetype='application/json')

def pending_request(request):
    if request.method == 'POST':
        user = request.POST.get('u_id')
        reqs = __pending_request(user)
        res = success("Got all the pending requests.")
        res['pending_reqs'] = reqs
    else:
        res = error("No request received.")
    return HttpResponse(dumps(res), mimetype='application/json')

def retrieve_f_request(request):
    if request.method == 'POST':
        f_er = request.POST.get('f_er')
        f_ed = request.POST.get('f_ed')

        res = __retrieve_f_request(f_er, f_ed)
    else:
        res = error("No request received.")

    return HttpResponse(dumps(res), mimetype='application/json')

def nearby(request):
    if request.method == 'POST':
        user = request.POST.get('u_id')
        res = __nearby(user)
    else:
        res = error("No request received.")
        
    return HttpResponse(dumps(res), mimetype='application/json')

## Methods related to checking in. ##

def check_in(request):
    if request.method == 'POST':
        u_id = request.POST.get('u_id')
        lat = request.POST.get('lat')
        lng = request.POST.get('lng')
        comm = request.POST.get('comm')

        #verify user exists
        user_exists = get_pk_user(u_id)
        if(is_Success(user_exists)):
            res = __check_in(lng, lat, u_id, comm)
            
        else:
            res = error(user_exists['msg'])
        
        return HttpResponse(dumps(res), mimetype='application/json')
    else:
        err = error("No request received")
        return HttpResponse(dumps(err), mimetype='application/json')

def show_checkins(request):
    if request.method == 'POST':
        u_id = request.POST.get('u_id')

        res = __show_checkins(u_id)

        return HttpResponse(dumps(res), mimetype='application/json')

    else:
        return HttpResponse(dumps(error("No request received.")), mimetype='application/json')

## Twilio ##

def send_info(request):
    if request.method == 'GET':
        number = request.GET.get('number')
        if(number is not None):
            number.replace(' ','')
            res = sendSMS(number)

            return HttpResponse(res, mimetype='application/json')
        else:
            return HttpResponse(dumps(error("No number received.")), mimetype='application/json')
    else:
        return HttpResponse(dumps(error("No request received")), mimetype='application/json')

def update_sensitivity(request):
    if request.method == 'POST':
        sensitivity_str = request.POST.get('sensitivity')
        user = request.POST.get('u_id')
        try:
            sensitivity = float(sensitivity_str)
            res = __update_sensitivity(user, sensitivity)

            return HttpResponse(dumps(res), mimetype='application/json')
        except Exception as inst:
            res = error("Error. %s" % inst)
            return HttpResponse(dumps(res), mimetype='application/json')
    else:
        return HttpResponse(dumps(error("No request received")), mimetype='application/json')        


def get_sensitivity(request):
    if request.method == 'POST':
        user = request.POST.get('u_id')
        resp = __get_sensitivity(user)

        return HttpResponse(dumps(resp), mimetype='application/json')
    else:
        return HttpResponse(dumps(error("No request received")), mimetype='application/json')

## Auth ##

def notify(request):
    if request.method == 'POST':
        u_id = request.POST.get('u_id')
        device = request.POST.get('device')
        payload = request.POST.get('payload')

        user_exists = get_pk_user(u_id)
        print user_exists

        if(user_exists['status'] == 'success'):
            tok = get_token(u_id, device)
            res = send_push(str(tok), str(payload))

        elif(user_exists['status'] == 'error'):
            res = error(user_exists['msg'])

        return HttpResponse(dumps(res), mimetype='application/json')

    else:
        return HttpResponse(dumps(error("No request received")), mimetype='application/json')

def poke(request):
    if request.method == 'POST':
        poke_er = request.POST.get('poke_er')
        poke_ed = request.POST.get('poke_ed')
        res = __poke(poke_er, poke_ed)

        return HttpResponse(dumps(res), mimetype='application/json')

    else:
        return HttpResponse(dumps(error("No request received")), mimetype='application/json')

def add_incognito(request):
    if request.method == 'POST':
        u_id = request.POST.get('u_id')
        lng = request.POST.get('lng')
        lat = request.POST.get('lat')

        if(is_Success(get_pk_user(u_id))):
            res = __add_incognito(u_id, lng, lat)
        else:
            res = error("No user %s" % u_id)

        return HttpResponse(dumps(res), mimetype='application/json')
    else:
        return HttpResponse(dumps(error("No request received")), mimetype='application/json')



