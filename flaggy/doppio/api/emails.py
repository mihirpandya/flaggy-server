from django.core.mail import send_mail, EmailMessage
from jinja2 import Environment, ChoiceLoader, FileSystemLoader
from json import dumps
import jinja2
import jinja2python
from jinja2python import render_to_response, render_to_string

#import doppio.api.controllers

emails = { }

emails['welcome'] = {
                       'subject': 'Welcome to Flaggy!',
                       'content': render_to_string('email_templates/welcome.html')
                    }

def follow_email(follower, key):
    result = { }
    result['subject'] = "%s wants to follow you on Flaggy!" % follower

    approve_url = "http://flaggyapp.com/approve_request?approval=1&k=%s" % key
    
    follow_content = render_to_string('email_templates/follow.html')
    
    follow_sub = follow_content.split("Insert subject here")
    follow_sub.append(follow_sub[1])
    follow_sub[1] = result['subject']

    follow_content = ""
    
    i = 0

    while i < len(follow_sub):
       follow_content = follow_content+follow_sub[i]
       i+=1
    
    follow_key = follow_content.split("approve_url")
    follow_key.append(follow_key[1])
    follow_key[1] = approve_url

    follow_content = ""

    i = 0

    while i < len(follow_key):
        follow_content = follow_content+follow_key[i]
        i+=1
    
    result['content'] = follow_content

    return result

def flaggy_email(info_obj):
    print info_obj
    try:
        if(info_obj['template'] == 'follow'):
            follower = info_obj['follower']
            key = info_obj['key']
            email_obj = follow_email(follower, key)

        else:
            template = info_obj['template']
            email_obj = emails[template]

        html_content = email_obj['content']

        msg = EmailMessage(email_obj['subject'],
                           html_content,
                           "notification@flaggyapp.com",
                           [info_obj['recipient']]
                           )
        msg.content_subtype = "html"

        if(msg.send() == 1):
            return success("Sent Welcome Email.")

    except Exception as inst:
        err = str(inst)
        return error(err)

def success(msg):
    return {'status': 'success', 'msg': msg}


def error(msg):
    return {'status': 'error', 'msg': msg}