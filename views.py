from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import json
from django.utils.crypto import get_random_string

import rsa
from User.models import User
from Bottle.models import Bottle
from User.sendsms import send_sms, sms_state_handler
# Create your views here.
# 调用该函数发送sms并将telephone和code存入cache中
def send_sms_view(request):
    code = get_random_string(length=4, allowed_chars="0123456789")
    params = "{\"code\":\"" + code + "\"}"
    tele = str(request.GET.get('telephone'))
    sms_result = sms_state_handler(send_sms(tele,params))

    if sms_result["code"] == 1:
        cache.set(tele, code, timeout=600)
    return HttpResponse(json.dumps(sms_result, ensure_ascii=False),content_type="application/json,charset=utf-8")

def register(request):
    if(request.method == "POST"):
        result = json.loads(request.body)
        username = result["username"]
        password = result["password"]
        phonenumber = result["phonenumber"]
        code = result["code"]

        # check if phonenumber corresponds to code
        if code != cache.get(phonenumber):
            result = {"code":0,"message":"验证码错误"}
            return HttpResponse(json.dumps(result,ensure_ascii=False),
                                content_type="application/json,charset=utf-8")

        # phonenumber existed
        if User.objects.filter(phonenumber=phonenumber):
            result = {"code":0,"message":"手机号已被注册"}
            return HttpResponse(json.dumps(result,ensure_ascii=False),
                                content_type="application/json,charset=utf-8")

        # username existed
        if User.objects.filter(username=username):
            result = {'code':0,"message":"用户名已被注册"}
            return HttpResponse(json.dumps(result,ensure_ascii=False),
                                content_type="application/json,charset=utf-8")

        # success
        user = User(username=username, password=password, phonenumber=phonenumber)
        user.save()

        result = {'code':1,"message":"success"}
        return HttpResponse(json.dumps(result,ensure_ascii=False),
                            content_type="application/json,charset=utf-8")

from django.db.models import Q
def login(request):
    if request.method == 'POST':
        # p = request.session['rsa']
        # prikey = rsa.PrivateKey.load_pkcs1(p.encode('utf-8'))
        # username为用户名或手机号
        json_result = json.loads(request.body)
        username = json_result['username']
        password = json_result['password']
        # password = rsa.decrypt(password,prikey)
        print(username)
        if not User.objects.filter(Q(username=username)|Q(phonenumber=username)).filter(isdeleted=False):
            return HttpResponse(json.dumps({
                    'msg': 'no such user'
                }), content_type="application/json")
        if not User.objects.filter(Q(username=username)|Q(phonenumber=username)).filter(password=password).filter(isdeleted=False):
            return HttpResponse(json.dumps({
                    'msg': 'wrong password'
                }), content_type="application/json")
        user = User.objects.filter(Q(username=username)|Q(phonenumber=username)).filter(isdeleted=False).first()
        request.session['username'] = user.username

        bottlenum = cache.get('bottlenum')
        if not bottlenum:   
            bottlenum = Bottle.objects.all().count()
            cache.set("bottlenum", bottlenum, 60)

        return HttpResponse(json.dumps({
            "msg" : "success",
            "bottlenum" : bottlenum,
            "issuper" : user.issuper,
        }), content_type="application/json")

def get_user_infos(request):
    if request.method == 'GET':
        username = request.session.get('username')
        user = User.objects.get(username=username)
        return HttpResponse(json.dumps({
            "msg" : "success",
            "username" : user.username,
            "phonenumber" : user.phonenumber,
            "address" : user.addresses,
            "credit" : user.credit,
            "enrolldatetime" : user.enrolldatetime.strftime("%Y-%m-%d %H:%M:%S"),
            "issuper" : user.issuper,
        }), content_type="application/json")

from Bottle.views import get_bottle_info
def get_star_infos(request):
    if request.method == 'POST':
        username = request.session.get('username')
        user = User.objects.get(username=username)
        stars = user.star.all()
        bids = []
        for bottle in stars:
            bids.append(get_bottle_info(bottle))
        return HttpResponse(json.dumps({
            "msg" : "success",
            "bottles" : bids
        }), content_type="application/json")

def add_star(request):
    if request.method == 'POST':
        username = request.session.get('username')
        user = User.objects.get(username=username)
        json_result = json.loads(request.body)
        botid = json_result['botid']
        user.star.add(botid)
        return HttpResponse(json.dumps({
            "msg":"success" 
            }), content_type="application/json")

def del_star(request):
    if request.method == 'POST':
        username = request.session.get('username')
        user = User.objects.get(username=username)
        json_result = json.loads(request.body)
        botid = json_result['botid']
        user.star.remove(botid)
        return HttpResponse(json.dumps({
            "msg":"success" 
            }), content_type="application/json")

def update_addresses(request):
    if request.method == 'POST':
        username = request.session.get('username')
        user = User.objects.get(username=username)
        json_result = json.loads(request.body)
        user.addresses = json_result['new_address']
        user.save()
        return HttpResponse(json.dumps({
            "msg":"success" 
            }), content_type="application/json")

def get_public_key(request):
    if request.method=='GET':
        pubkey, prikey = rsa.newkeys(1024)
        pub = pubkey.save_pkcs1()
        pri = prikey.save_pkcs1()
        request.session["rsa"] = pri.decode('utf-8')
        return HttpResponse(json.dumps({
            "msg":"success",
            "pubkey": pub.decode('utf-8'),
            }), content_type="application/json")