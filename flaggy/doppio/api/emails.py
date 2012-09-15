from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMessage
#import doppio.api.controllers

emails = { }

emails['welcome'] = {
                       'subject': 'Welcome to Flaggy!',
                       'content': render_to_string('email/welcome.html')
                    }

def follow_email(follower, key):
    result = { }
    result['subject'] = "%s wants to follow you on Flaggy!" % follower

    approve_url = "http://flaggy-mihirmp.dotcloud.com/approve_request?k=%s" % key
    
    follow_content = render_to_string('email/follow.html')
    
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
    try:
        if(info_obj['template'] == 'follow'):
            follower = info_obj['follower']
            key = info_obj['key']
            email_obj = follow_email(follower, key)

        else:
            template = info_obj['template']
            email_obj = emails[template]['content']

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
        err = "Failed to send email. Exception: %s" % str(inst)
        return error(err)

def success(msg):
    return {'status': 'success', 'msg': msg}


def error(msg):
    return {'status': 'error', 'msg': msg}