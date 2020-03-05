from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin
import json
class LoginInterception(MiddlewareMixin):

    def process_request(self, request):
        print(request.path)
        if request.path=='/user/change_password/':
            try:
                request.session['username']
            except Exception:
                return HttpResponse(json.dumps({ 
                    "msg":"session expired"
                }), content_type="application/json")