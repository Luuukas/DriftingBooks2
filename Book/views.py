from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.cache import cache
from django.views.decorators.cache import cache_page
import json

from User.models import User
from Book.models import Book
from Book.douban_book import get_book_info
def crawl_worker(isbn):
    '''
    book = {
        '封面图': img,
        '内容简介': content_intro,
        '作者简介': author_intro,
        '书名': name,
        '作者': '无',
        '译者': '无',
        '出版社': '无',
        '原作名': '无',
        '出版年': '无',
        '页数': '无',
        '定价': '无',
        '装帧': '无',
        '丛书': '无',
        'ISBN': '无',
        }
    '''
    book_info = get_book_info(isbn)
    # print(book_info)
    if book_info==None:
        return False
    book = Book.objects.create(isbn=isbn)
    book.bookname = book_info['书名']
    book.origin_bookname = book_info['原作名']
    book.writer = book_info['作者']
    book.translator = book_info['译者']
    book.pagenum = book_info['页数']
    book.publishtime = book_info['出版年']
    book.price = book_info['定价']
    book.content_intro = (book_info['内容简介'] if len(book_info['内容简介'])<253 else book_info['内容简介'][0:253]+"..."),
    book.writer_intro = (book_info['作者简介'] if len(book_info['作者简介'])<253 else book_info['作者简介'][0:253]+"..."),
    book.coverurl = book_info['封面图']
    book.press = book_info['出版社']

    book.save()

    return True

def crawl_book_infos(isbn):
    if Book.objects.filter(isbn=isbn) or crawl_worker(isbn):
        return Book.objects.get(isbn=isbn)
    return None

# Create your views here.
def get_book_infos(request):
    if request.method == 'POST':
        json_result = json.loads(request.body)
        book = Book.objects.get(id=json_result['bokid'])
        return HttpResponse(json.dumps({
            "msg" : "success",
            "isbn" : book.isbn,
            "bookname" : book.bookname,
            "origin_bookname" : book.origin_bookname,
            "writer" : book.writer,
            "translator" : book.translator,
            "pagenum" : book.pagenum,
            "publishtime" : book.publishtime,
            "price" : book.price,
            "content_intro" : book.content_intro,
            "writer_intor" : book.writer_intro,
            "neededcredit" : book.neededcredit,
        }), content_type="application/json")

def define_book_neededcredit(request):
    if request.method == 'POST':
        json_result = json.loads(request.body)
        username = request.session.get("username")
        user = User.objects.get(username=username)
        if not user.issuper:
            return HttpResponse(json.dumps({ 
                "msg":"has no right"
            }), content_type="application/json")
        
        isbn = json_result['isbn']
        neededcredit = json_result['neededcredit']

        book = crawl_book_infos(isbn)

        if not book:
            return HttpResponse(json.dumps({ 
                "msg":"no such book"
            }), content_type="application/json")

        book.neededcredit = neededcredit
        book.save()
        return HttpResponse(json.dumps({ 
            "msg":"success"
        }), content_type="application/json")
