# search book number from DouBan

import requests
from lxml import etree

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}

data = {
    'cat': '1001',
    'search_text': '',  # 'search_text' 例：'解忧杂货店 东野圭吾 南海出版公司'

}


def get_url_book_number(isbn):
    data['search_text'] = isbn
    html = requests.get('http://douban.com/isbn/'+isbn+'/', headers=headers)
    return html.url
