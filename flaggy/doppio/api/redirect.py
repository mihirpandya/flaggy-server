from django.http import HttpResponse, HttpResponseRedirect

client_id="D1CWI4INWDWCSHN4C4WZKQSY0XCGF4GQZZUAJHIDAWVS5E2P"
client_secret="DCNXKCBKWRL3IHYXJS33LV5WXZFKOH0KA1PZOJSHDHOJUGT4"
redirect_uri="flaggy-mihirmp.dotcloud.com"
approve_uri="localhost:8000/foursquare_approve"

def authenticate(request):
	url="https://foursquare.com/oauth2/authenticate?client_id="+client_id+"&response_type=code&redirect_uri="+redirect_uri
	return HttpResponseRedirect(url)

def redirect(request):
	if(request.method == 'GET'):
		code = request.GET.get('code')
		url="https://foursquare.com/oauth2/access_token?client_id="+client_id+"&client_secret="+client_secret+"&grant_type=authorization_code&redirect_uri="+approve_uri+"&code="+code
		return HttpResponseRedirect(url)

	else:
		return HttpResponse(dumps(error("Error. No request received.")), mimetype='application/json')
		
def foursquare_approve(request):
	data =HttpRequest.read()
	print data