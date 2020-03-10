# test.py

# uwsgi --http :8000 --wsgi-file uWSGItest.py
# the web client <-> uWSGI <-> Python

# uwsgi --http :8000 --module mysite.wsgi
# the web client <-> uWSGI <-> Django

# uwsgi --socket :8001 --wsgi-file test.py
# 访问http://xxx.xxx.xxx.xxx
# the web client <-> the web server <-> the socket <-> uWSGI <-> Python
def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])
    # return ["Hello World"] # python2
    return [b"Hello World"] # python3