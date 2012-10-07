import base64, urllib2
from json import loads
from doppio.api.controllers import error

user = 'AC2d3fabac57f4c44d8929ac52d34c58d8'
password = '27ffc2282e1fb30bcf524d6841ef8ed2'
url = "https://api.twilio.com/2010-04-01/Accounts/AC2d3fabac57f4c44d8929ac52d34c58d8/SMS/Messages.json"

def sendSMS(number):
	request = urllib2.Request(url)
	
	interm_base64string = base64.encodestring('%s:%s' % (user, password))
	base64string = interm_base64string.replace('\n', '')
	request.add_header("Authorization", "Basic %s" % base64string)

	text_content = "Thanks for your interest in Flaggy! Download Flaggy from the App Store from this link http://flaggy-mihirmp.dotcloud.com"
	
	post_data = 'From=%2B14129234256&To=%2B'+number+'&Body='+text_content
	request.add_data(post_data)
	
	try:
		result = urllib2.urlopen(request)
		res = result.read()
	
	except Exception as inst:
		res = error("Error. Couldn't send text: %s" % inst)

	return res