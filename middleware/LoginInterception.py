from django.http import HttpResponse
from django.utils.deprecation import MiddlewareMixin

class LoginInterception(MiddlewareMixin):

    def process_request(self, request):
        print(request.path)