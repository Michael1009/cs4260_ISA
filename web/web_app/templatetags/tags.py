from django import template
import urllib.request, json
register = template.Library()


@register.simple_tag
def get_name(request):
    resp_dict = get_user_info(request)
    return resp_dict['first_name']

def get_user_info(request):
    post_data = {'auth': request.COOKIES.get("auth")}
    data = urllib.parse.urlencode(post_data).encode("utf-8")
    req = urllib.request.Request('http://exp:8000/exp/info/')
    with urllib.request.urlopen(req,data=data) as f:
        resp = f.read()
    
    resp_text = resp.decode('utf-8')
    resp_dict = json.loads(resp_text)
    return resp_dict