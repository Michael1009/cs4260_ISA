from django import template
import urllib.request, json


def get_if_logged_in(request):
	auth = request.COOKIES.get("auth")
	logged_in = True
	if not auth: logged_in = False
	if logged_in:
		post_data = {'auth': request.COOKIES.get("auth")}
		data = urllib.parse.urlencode(post_data).encode("utf-8")
		req = urllib.request.Request('http://exp:8000/exp/info/')
		with urllib.request.urlopen(req,data=data) as f:
				resp = f.read()
		
		resp_text = resp.decode('utf-8')
		resp_dict = json.loads(resp_text)

		return {'logged_in':True, 'first_name':resp_dict['first_name']}
	else: return {'logged_in': False}