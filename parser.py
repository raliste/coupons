"""
Coupon Finder

The MIT License

Copyright (c) 2011 Rodrigo Aliste P <raliste@googlemail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import urllib2
import re
from BeautifulSoup import BeautifulSoup

USER_AGENT = 'CouponFinder/0.1; +http://coupons.com/coupons.html'

# Utils

_opener = urllib2.build_opener()

def test_groupon():
  urls = get_urls_groupon(get_url('http://www.groupon.cl/deals/recent/santiago-centro'))
  for url in urls:
    html = get_url(url[0])
    print parse_groupon(html)

def get_url(url):
  try:
    request = urllib2.Request(url)
    request.add_header('User-Agent', USER_AGENT)

    html = _opener.open(request).read()
    
    return html
  except urllib2.HTTPError, e:
    print e.code
    print e.read()

def remove_non_numeric(number):
  return re.sub('[^0-9]+', '', number)

# Coupons finders

def get_urls_groupon(html):
  soup = BeautifulSoup(html)
  
  urls = list()
  
  listing = soup.find('ul', {'class': 'recent-deals'}).findAll('li')
  for item in listing:
    url = item.find('a', {'class': 'title'}).get('href')
    date = item.find('span', {'class': 'date'}).string

    urls.append((url, date))
    
  return urls

# Parsers

def parse_groupon(html):
  soup = BeautifulSoup(html)

  title = soup.find('h1', {'class': 'title'}).string
  numbers = soup.find('ul', {'class': 'numbers'}).findAll('li')

  original_price = remove_non_numeric(numbers[0].span.string)
  discount = remove_non_numeric(numbers[1].span.string)

  return title, original_price, discount

def parse_letsbonus(html):
  soup = BeautifulSoup(html)

  title = soup.find('h1', {'class': 'frontTitle'}).string
  numbers = soup.find('div', {'class': 'values'}).findAll('div')

  original_price = remove_non_numeric(numbers[0].findAll('span')[1].string)
  discount = remove_non_numeric(numbers[1].findAll('span')[1].string)

  return title, original_price, discount
  
if __name__ == '__main__':
  test_groupon()
