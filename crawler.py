import time
from lxml import html
import requests
import datetime
from slugify import slugify

class Crawler:
    def __init__(self, url):
        print 'Crawler is running on: ' + url
        self.url = url
        self.mailer = Mailer()
        self.posts = {}

        self.crawl()

        while True:
            time.sleep(60 * 10)
            self.crawl(True)

    def get_page(self, url):
        return requests.get(url).text


    def get_page_content(self, page):
        return html.fromstring(page)

    def crawl(self, notify=False):
        print 'Crawling ' + str(datetime.datetime.now().time())
        page = self.get_page(self.url)
        tree = self.get_page_content(page)

        posts = tree.cssselect('.content .row .txt')

        res = ''
        for p in posts:
            txt = p.cssselect('.pl a')[0].text
            href = p.cssselect('.pl a')[0].attrib['href']
            href = self.url + href.split('/sfc/sub/')[1]
            price = p.cssselect('.price')

            if len(price) > 0:
                price = price[0].text
            else:
                price = 'No price'

            if self.get_key(txt) not in self.posts:
                res += '**: %s - %s - %s\n\n' %(txt, price, href)
                self.posts[self.get_key(txt)] = True


        if notify and res != '':
            self.mailer.send(res)

    def get_key(self, key):
        return slugify(key)



class Mailer(object):
    def __init__(self):
        pass

    def send(self, content):
        r = requests.post(
        "https://api:key-9810xd55u8zl19jxwlj4139t3tbntu75@api.mailgun.net/v2/sandbox95861668de88460d888b9c233edfd5d3.mailgun.org/messages",
        auth=("api", ""),
        data={"from": "NEW-ADD <nothing@example.com>",
              "to": ["kim.a.pettersen@gmail.com"],
              "subject": "New Craiglsit add",
              "text": content})

        return r.status_code




if __name__ == '__main__':
    crawler = Crawler('http://sfbay.craigslist.org/sfc/sub/')


