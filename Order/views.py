from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import json
from datetime import datetime
from Order.models import receiveOrder, retriveOrder, acquireOrder
from User.models import User
from Bottle.models import Bottle

# Create your views here.
def fill_receive_order(request):
    if request.method == 'POST':
        username = request.session.get("username")
        user = User.objects.get(username=username)
        json_result = json.loads(request.body)
        trancode = json_result['transactioncode']
        receorder = receiveOrder.objects.filter(related_user__username=username).filter(transactioncode=trancode).first()
        if not receorder:
            return HttpResponse(json.dumps({ 
                "msg":"no such order"
            }), content_type="application/json")
        if not receorder.order_state==0:
            return HttpResponse(json.dumps({ 
                "msg":"not a incomplete order"
            }), content_type="application/json")

        receorder.expresscompany = json_result['expresscompany']
        receorder.trackingnumber = json_result['trackingnumber']
        receorder.order_state = 1
        receorder.dealtime = datetime.now()
        receorder.from_name = json_result['name']
        receorder.from_address = json_result['address']
        receorder.from_phonenumber = json_result['phonenumber']
        receorder.save()

        return HttpResponse(json.dumps({ 
            "msg" : "success" 
            }), content_type="application/json")

def accept_book_order(request):
    if request.method == 'POST':
        username = request.session.get("username")
        user = User.objects.get(username=username)
        json_result = json.loads(request.body)
        if not user.issuper:
            return HttpResponse(json.dumps({ 
                "msg":"has not right"
            }), content_type="application/json")

        trancode = json_result['transactioncode']
        receorder = receiveOrder.objects.get(transactioncode=trancode)
        if not receorder.order_state==1:
            return HttpResponse(json.dumps({ 
                "msg":"not a complete order"
            }), content_type="application/json")

        receorder.related_bottle.book_state = 2
        receorder.dealtime = datetime.now()
        receorder.save()
        receorder.related_bottle.save()
        return HttpResponse(json.dumps({ 
            "msg":"success"
            }), content_type="application/json")

def reject_book_order(request):
    if request.method == 'POST':
        username = request.session.get("username")
        user = User.objects.get(username=username)
        json_result = json.loads(request.body)
        if not user.issuper:
            return HttpResponse(json.dumps({ 
            "msg":"has not right"
            }), content_type="application/json")
        trancode = json_result['transactioncode']
        receorder = receiveOrder.objects.get(transactioncode=trancode)
        if not receorder.order_state==1:
            return HttpResponse(json.dumps({ 
                "msg":"not a complete order"
            }), content_type="application/json")

        receorder.related_bottle.book_state = 3
        receorder.dealtime = datetime.now()
        receorder.save()
        receorder.related_bottle.save()
        return HttpResponse(json.dumps({ 
            "msg":"success"
            }), content_type="application/json")

def retrive_book(request):
    if request.method == 'POST':
        username = request.session.get("username")
        user = User.objects.get(username=username)
        json_result = json.loads(request.body)
        botid = json_result['botid']
        bottle = Bottle.objects.get(id=botid)
        if not bottle.book_state==3:
            # 仅当已拒收的状态的书可被取回，取回后状态变为0
            return HttpResponse(json.dumps({ 
                "msg":"cannot be retrieve"
            }), content_type="application/json")

        receorder = receiveOrder.objects.get(related_bottle__id=botid)

        retrorder = retriveOrder.objects.create(related_bottle=bottle, related_user=user)
        retrorder.to_address = receorder.from_address
        retrorder.to_name = receorder.from_name
        retrorder.to_phonenumber = receorder.from_phonenumber
        retrorder.save()

        bottle.book_state = 0
        bottle.save()
        return HttpResponse(json.dumps({ 
            "msg":"success"
            }), content_type="application/json")

def get_order_infos(order, trancode):
    if trancode==None:
        trancode = order.transactioncode
    if str(trancode)[0:4] == "RECE":
        if order == None:
            order = receiveOrder.objects.get(transactioncode=trancode)
        return {
                "otype" : 0,
                "expresscompany" : order.expresscompany,
                "trackingnumber" : order.trackingnumber,
                "order_state" : order.order_state,
                "submittime" : order.submittime.strftime("%Y-%m-%d %H:%M:%S"),
                "dealtime" : (order.dealtime.strftime("%Y-%m-%d %H:%M:%S") if order.dealtime else None),
                "related_bottle" : order.related_bottle.id,
                "related_user" : order.related_user.username,
                "transactioncode" : order.transactioncode,
                "name" : order.from_name,
                "address" : order.from_address,
                "phonenumber" : order.from_phonenumber,
                "brief_book_infos" : {
                    "bookname" : order.related_bottle.related_book.bookname,
                    "writer" : order.related_bottle.related_book.writer,
                    "press" : order.related_bottle.related_book.press,
                    "neededcredit" : order.related_bottle.related_book.neededcredit,
                    "coverurl" : order.related_bottle.related_book.coverurl,
                    'description': order.related_bottle.related_book.content_intro,
                }
            }
    elif str(trancode)[0:4] == "RETR":
        if order == None:
            order = retriveOrder.objects.get(transactioncode=trancode)
        return {
                "otype" : 1,
                "expresscompany" : order.expresscompany,
                "trackingnumber" : order.trackingnumber,
                "order_state" : order.order_state,
                "submittime" : order.submittime.strftime("%Y-%m-%d %H:%M:%S"),
                "dealtime" : (order.dealtime.strftime("%Y-%m-%d %H:%M:%S") if order.dealtime else None),
                "related_bottle" : order.related_bottle.id,
                "related_user" : order.related_user.username,
                "transactioncode" : order.transactioncode,
                "name" : order.to_name,
                "address" : order.to_address,
                "phonenumber" : order.to_phonenumber,
                "brief_book_infos" : {
                    "bookname" : order.related_bottle.related_book.bookname,
                    "writer" : order.related_bottle.related_book.writer,
                    "press" : order.related_bottle.related_book.press,
                    "neededcredit" : order.related_bottle.related_book.neededcredit,
                    "coverurl" : order.related_bottle.related_book.coverurl,
                    'description': order.related_bottle.related_book.content_intro,
                }
            }
    elif str(trancode)[0:4] == "ACQU":
        if order == None:
            order = acquireOrder.objects.get(transactioncode=trancode)
        return {
                "otype" : 2,
                "expresscompany" : order.expresscompany,
                "trackingnumber" : order.trackingnumber,
                "order_state" : order.order_state,
                "submittime" : order.submittime.strftime("%Y-%m-%d %H:%M:%S"),
                "dealtime" : (order.dealtime.strftime("%Y-%m-%d %H:%M:%S") if order.dealtime else None),
                "related_bottle" : order.related_bottle.id,
                "related_user" : order.related_user.username,
                "transactioncode" : order.transactioncode,
                "name" : order.to_name,
                "address" : order.to_address,
                "phonenumber" : order.to_phonenumber,
                "brief_book_infos" : {
                    "bookname" : order.related_bottle.related_book.bookname,
                    "writer" : order.related_bottle.related_book.writer,
                    "press" : order.related_bottle.related_book.press,
                    "neededcredit" : order.related_bottle.related_book.neededcredit,
                    "coverurl" : order.related_bottle.related_book.coverurl,
                    'description': order.related_bottle.related_book.content_intro,
                }
            }

def get_order(request):
    if request.method == 'POST':
        json_result = json.loads(request.body)
        trancode = json_result['transactioncode']
        return HttpResponse(json.dumps({
            "msg" : "success",
            "infos" : get_order_infos(None, trancode),
        }), content_type="application/json")
        
def get_orders_of_user(request):
    if request.method == 'POST':
        username = request.session.get("username")
        user = User.objects.get(username=username)
        orders = []
        receorder = receiveOrder.objects.filter(related_user__username=username)
        retrorder = retriveOrder.objects.filter(related_user__username=username)
        acquorder = acquireOrder.objects.filter(related_user__username=username)
        for order in receorder:
            orders.append(get_order_infos(order, None))
        for order in retrorder:
            orders.append(get_order_infos(order, None))
        for order in acquorder:
            orders.append(get_order_infos(order, None))
        return HttpResponse(json.dumps({
            "msg" : "success",
            "orders" : orders
        }), content_type="application/json")

def get_all_orders(request):
    if request.method == 'POST':
        username = request.session.get("username")
        user = User.objects.get(username)
        if not user.issuper:
            return HttpResponse(json.dumps({ 
                "msg":"has not right"
            }), content_type="application/json")

        orders = []
        receorder = receiveOrder.objects.all()
        retrorder = retriveOrder.objects.all()
        acquorder = acquireOrder.objects.all()
        for order in receorder:
            orders.append(get_order_infos(order, None))
        for order in retrorder:
            orders.append(get_order_infos(order, None))
        for order in acquorder:
            orders.append(get_order_infos(order, None))
        return HttpResponse(json.dumps({
            "msg" : "success",
            "orders" : orders
        }), content_type="application/json")