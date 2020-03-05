from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import json

from Bottle.models import Bottle
from Book.views import crawl_book_infos
from User.models import User

import os
from django.conf import settings
import time

# Create your views here.
def get_bottle_num(request):
    bottlenum = Bottle.objects.all().count()
    cache.set("bottlenum", bottlenum, 60)
    if request.method == 'GET':
        return HttpResponse(json.dumps({
            "msg" : "success",
            "bottlenum" : bottlenum,
        }), content_type="application/json")

def get_bottle_info(bottle):
    try:
        article_obj = open(bottle.article)
        article = article_obj.read()
        article_obj.close()
        return {
            "msg" : "success",
            "botid" : bottle.id,
            "bokid" : bottle.related_book.id,
            "bookname" : bottle.related_book.bookname,
            "writer" : bottle.related_book.writer,
            "press" : bottle.related_book.press,
            "description" : article,
            "photourls" : bottle.photos,
            "ispicked" : (bottle.book_sendto!=0),
            "isshared" : (bottle.book_sendto!=-1),  # 这个漂流瓶所描述的书，拥有者是否有把图书放出来，-1是没有
            "donatedto" : (bottle.book_sendto if bottle.book_sendto<-1 else 1),
            "uploaddatetime" : bottle.upload_datetime.strftime("%Y-%m-%d %H:%M:%S"),
            "state" : bottle.book_state,
        }
    except Exception:
        return json.dumps({
            "msg" : "fail to read the bottle",
        })
        
def vis_bottle(request):
    if request.method == 'POST':
        json_result = json.loads(request.body)
        idx = json_result["idx"]
        bottle = Bottle.objects.all()[idx-1];
        return HttpResponse(json.dumps(get_bottle_info(bottle)), content_type="application/json")

def get_bottle(request):
    if request.method == 'POST':
        json_result = json.loads(request.body)
        botid = json_result["botid"]
        bottle = Bottle.objects.get(id=botid)
        return HttpResponse(json.dumps(get_bottle_info(bottle)), content_type="application/json")

from Order.models import receiveOrder
def add_bottle(request):
    if request.method == 'POST':
        username = request.session.get("username")
        # 关联用户
        user = User.objects.get(username=username)
        isbn = request.POST.get("isbn")
        # 如果书库中没有记录isbn，则让爬虫去爬，如果isbn无效则直接返回，有效则把爬回来的信息加入书库
        book = crawl_book_infos(isbn)
        if not book:
            return HttpResponse(json.dumps({
                 "msg" : "no such book" 
                 }), content_type="application/json")
        bottle = Bottle.objects.create(related_book=book, related_user=user)
        # 把文本写入txt中存储
        article = request.POST.get('description')
        article_name = "des_"+str(time.time())+".txt"
        article_path = os.path.join(settings.BASE_DIR, 'static', 'des', article_name)
        with open(article_path, 'w') as f:
            f.write(article)
        bottle.article = article_path
        # 存储图片，有可能没有图片
        try:
            img_obj = request.FILES.get('img_obj')
            postfix = img_obj.name.split('.')[1]
            img_name = "img_"+str(time.time())+"."+postfix
            img_path = os.path.join(settings.BASE_DIR, 'static', 'img', img_name)
            img_url = os.path.join(settings.SERVER_DIR, img_name)
            with open(img_path, 'wb') as f:
                for chunk in img_obj.chunks():
                    f.write(chunk)
                    f.flush()
        except Exception:
            img_url = ""
        bottle.photos = img_url
        bottle.book_sendto = request.POST.get('sendto')

        if request.POST.get('sendto')!=-1:
            receorder = receiveOrder.objects.create(related_bottle=bottle, related_user=user)
            bottle.book_state = 1
            receorder.save()

        bottle.save()

        return HttpResponse(json.dumps({
            "msg" : "ok",
            "transactioncode" : (receorder.transactioncode if receorder else None),
            }), content_type="application/json")

def can_pick(bottle):
    return (bottle.book_state==2 and bottle.book_sendto==0 and bottle.related_book.neededcredit>-1)

from Order.models import acquireOrder
def pick_bottle_book(request):
    if request.method == 'POST':
        username = request.session.get("username")
        user = User.objects.get(username=username)
        json_result = json.loads(request.body)
        botid = json_result['botid']
        bottle = Bottle.objects.get(id=botid)
        
        if not can_pick(bottle):
            return HttpResponse(json.dumps({
                "msg":"invalid operation"
                }), content_type="application/json")

        if user.credit < bottle.related_book.neededcredit:
            return HttpResponse(json.dumps({ 
                "msg":"not enought credit" 
                }), content_type="application/json")

        acquorder = acquireOrder.objects.create(related_user=user, related_bottle=bottle)
        acquorder.to_address = json_result['address']
        acquorder.to_name = json_result['name']
        acquorder.to_phonenumber = json_result['phonenumber']
        acquorder.save()

        bottle.book_sendto = user.id
        bottle.save()

        user.credit = user.credit - bottle.related_book.neededcredit
        user.save()

        return HttpResponse(json.dumps({ 
            "msg" : "success", 
            "transactioncode" : acquorder.transactioncode,
            }), content_type="application/json")
