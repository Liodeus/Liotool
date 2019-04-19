import sys
import myparser
import time
import requests
from discovery.constants import *

class search_bing:

    def __init__(self, word, limit, start):
        self.word = word.replace(' ', '%20')
        self.results = ""
        self.totalresults = ""
        self.server = "www.bing.com"
        self.apiserver = "api.search.live.net"
        self.hostname = "www.bing.com"
        self.quantity = "50"
        self.limit = int(limit)
        self.bingApi = ""
        self.counter = start

    def do_search(self):
        headers = {
            'Host': self.hostname,
            'Cookie':'SRCHHPGUSR=ADLT=DEMOTE&NRSLT=50',
            'Accept-Language': 'en-us,en',
            'User-agent': getUserAgent()
        }
        h = requests.get(url=('http://'+self.server + "/search?q=%40" + self.word + "&count=50&first=" + str(self.counter)),headers=headers)
        self.results = h.text
        self.totalresults += self.results

    def do_search_api(self):
        url = 'http://' + self.server + "/xml.aspx?Appid="+self.bingApi+"&query=%40" + \
               self.word + "&sources=web&web.count=40&web.offset=" + str(self.counter)
        headers = {
            'Host': self.apiserver,
            'User-agent': getUserAgent()
        }
        h = requests.get(url=url, headers=headers)
        self.results = h.text
        self.totalresults += self.results

    def do_search_vhost(self):
        headers = {
            'Host': self.hostname,
            'Cookie': 'mkt=en-US;ui=en-US;SRCHHPGUSR=NEWWND=0&ADLT=DEMOTE&NRSLT=50',
            'Accept-Language': 'en-us,en',
            'User-agent': getUserAgent()
        }
        url = 'http://' + self.server + "/search?q=ip:" + self.word + "&go=&count=50&FORM=QBHL&qs=n&first=" + str(self.counter)
        h = requests.get(url=url, headers=headers)
        self.results = h.text
        self.totalresults += self.results

    def get_emails(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.emails()

    def get_hostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames()

    def get_allhostnames(self):
        rawres = myparser.parser(self.totalresults, self.word)
        return rawres.hostnames_all()

    def process(self, api):
        if api == "yes":
            if self.bingApi == "":
                print("Please insert your API key in the discovery/bingsearch.py")
                sys.exit()
        while (self.counter < self.limit):
            if api == "yes":
                self.do_search_api()
                time.sleep(getDelay())
            else:
                self.do_search()
                time.sleep(getDelay())
            self.counter += 50
            print("\tSearching " + str(self.counter) + " results...")

    def process_vhost(self):
        # Maybe it is good to use other limit for this.
        while (self.counter < self.limit):
            self.do_search_vhost()
            self.counter += 50
