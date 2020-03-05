import requests
from lxml import etree
from Book.search import get_url_book_number

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'
    }

def get_name(et):
    t = (et.xpath('//*[@id="wrapper"]/h1/span/text()')[0])
    if t==[]:
        return '无'
    else:
        return t;

def get_img(et):  # 封面图
    t = (et.xpath('//*[@id="mainpic"]/a/img')[0])
    if t == []:
        img = '无'
        return img
    else:
        img = t.xpath('@src')[0]
        return img


def get_content_intro(et):  # 内容简介
    content = ''
    t = et.xpath('//*[@class="intro"]/descendant::p/text()')
    if t == []:
        content = '无'
        return content
    else:
        for i in t:
            content = content + i + '\n'
        return content


def get_author_intro(et):  # 作者简介
    author = ''
    t = et.xpath('//*[@class="indent "]/descendant::p/text()')
    if t == []:
        author = '无'
        return author
    else:
        for i in t:
            author = author + i + '\n'
        return author

import re
def get_book_info(isbn):
    try:
        url = get_url_book_number(isbn)
        html = requests.get(url, headers=headers)  # 'https://book.douban.com/subject/25862578/'
        bs = etree.HTML(html.text)

        img = get_img(bs)
        content_intro = get_content_intro(bs)
        author_intro = get_author_intro(bs)
        name = get_name(bs)

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

        strr = str(html.text).replace(' ','').replace('\n','')

        c = re.findall(r'<span><spanclass="pl">(.*?)</span>.*?<aclass=""href=".*?">(.*?)</a></span><br/>', strr)
        for a in c:
            spres = re.split(r'</a>/<aclass=""href="/search/.*?">',str(a[1]))
            label = str(a[0]).replace(':','')
            book[label] = spres[0]
            for i in range(1,len(spres)):
                book[label] = book[label] + "，" + spres[i]

        c = re.findall(r'<span class="pl">(.*?)</span>(.*?)<br/>', str(html.text))
        for a in c:
            label = str(a[0]).replace(':','')
            book[label] = str(a[1]).strip()

        return book
    except Exception:
        return None


# book = get_book_info('9787513337106')
# print(book)