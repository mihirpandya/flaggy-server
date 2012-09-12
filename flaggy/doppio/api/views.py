from doppio.models import User
from doppio.api.controllers import __add_user, __add_follow, __unfollow, __approve_request, __followers, __following, __check_in, verify_user, success, error, empty_str, last_check_in, __unapproved_requests, __retrieve_f_request, __approved_request
from json import dumps
from django.template import Context, loader
from datetime import datetime
from django.http import HttpResponse


def hello_view(request):
    """ Simple Hello World View """
    t = loader.get_template('helloworld.html')
    c = Context({
        'current_time': datetime.now(),
    })
    return HttpResponse(t.render(c))


def add_user(request):
    if request.method == 'GET':
        f_n = request.GET.get('fname')
        l_n = request.GET.get('lname')
        fb_id = request.GET.get('fb_id')
        email = request.GET.get('email')
        res = {}
        checkin_user = {}

        if verify_user(fb_id):
            u = User.objects.get(fb_id=fb_id)
            last_checkin = last_check_in(u.u_id)

            if last_checkin is not None:
                checkin_user = last_checkin

            res["status"] = 2
            res["msg"] = "User "+u.fname+" already exists!"
            res["last_checkin"] = checkin_user
            ## Add the last checkin location here
            res["u_id"] = str(u.u_id)
            ## We should return friends (you mean followers) if the user already exists ##
            res["following"] = __following(u.u_id)

        elif not empty_str(f_n) and not empty_str(l_n) and not empty_str(fb_id):
            add_status = __add_user(f_n, l_n, fb_id, 0000, email)
            
            if(add_status["status"] == "success"):
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


# accepts f_er, fb_ed, email_ed
def add_follow(request):
    if request.method == 'GET':
        follower = request.GET.get('f_er')
        followed_fb = request.GET.get('fb_ed')
        followed_email = request.GET.get('email_ed')

        if follower is not None and followed_fb is not None and followed_email is not None:
            res = __add_follow(follower, followed_fb, followed_email)
            return HttpResponse(dumps(res), mimetype='application/json')
        elif followed_fb is None:
            err = error("Facebook ID of the person you want to follow is missing.")
            return HttpResponse(dumps(err), mimetype='application/json')
        elif followed_email is None:
            err = error("Email of the person you want to follow is missing.")
            return HttpResponse(dumps(err), mimetype='application/json')

    else:
        err = error("No request received.")
        return HttpResponse(dumps(err), mimetype='application/json')


def approve_request(request):
    if request.method == 'GET':
        key = request.GET.get('k')
        res = __approve_request(key)
        return HttpResponse(dumps(res), mimetype='application/json')


def unfollow(request):
    if request.method == 'GET':
        f_er = request.GET.get('f_er')
        f_ed = request.GET.get('f_ed')
        res = __unfollow(f_er, f_ed)
        return HttpResponse(dumps(res), mimetype='application/json')


def followers(request):
    if request.method == 'GET':
        u_id = request.GET.get('u_id')
        res = __followers(u_id)
        if len(res) > 0:
            return HttpResponse(dumps(res), mimetype='application/json')
        else:
            return HttpResponse(dumps(None), mimetype='application/json')
    else:
        err = error("No request received.")
        return HttpResponse(dumps(err), mimetype='application/json')


def following(request):
    if request.method == 'GET':
        u_id = request.GET.get('u_id')
        res = __following(u_id)
        if len(res) > 0:
            return HttpResponse(dumps(res), mimetype='application/json')
        else:
            return HttpResponse(dumps(None), mimetype='application/json')
    else:
        err = error("No request received.")
        return HttpResponse(dumps(err), mimetype='application/json')


def check_in(request):
    if request.method == 'GET':
        u_id = request.GET.get('u_id')
        lat = request.GET.get('lat')
        lng = request.GET.get('lng')
        comm = request.GET.get('comm')
        res = __check_in(lng, lat, u_id, comm)
        return HttpResponse(dumps(res), mimetype='application/json')
    else:
        err = error("No request received")
        return HttpResponse(dumps(err), mimetype='application/json')

def unapproved_requests(request):
    if request.method == 'GET':
        res = __unapproved_requests()
        return HttpResponse(dumps(res), mimetype='application/json')

def approved_requests(request):
    if request.method == 'GET':
        res = __approved_request()
        return HttpResponse(dumps(res), mimetype='application/json')

def retrieve_f_request(request):
    if request.method == 'GET':
        f_er = request.GET.get('f_er')
        f_ed = request.GET.get('f_ed')

        res = __retrieve_f_request(f_er, f_ed)
        return HttpResponse(dumps(res), mimetype='application/json')
