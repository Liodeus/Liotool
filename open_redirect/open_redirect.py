#!/usr/bin/python
import requests
import sys

def start():
    domain = sys.argv[1]
    payload_file = sys.argv[2]

    payloads = open(payload_file,'r').read().split('\n')

    #First loop trough the payloads to prevent 429 (rate limit)
    for payload in payloads:   
        print "\n - Trying payload "+payload+" - "
        if domain != "":

            url = domain + payload
            url = url.strip()
        
            try:
                r = requests.head(url, allow_redirects=True, timeout=5)

                if r.history:  
                    if r.url == "https://example.com":
                        print "[+]"+url
                    else:
                        print "[-]"+url
                else:
                    print "[-]"+url
            except:
                print "[-]Error on " + url
        else:
            print "[-]Domain is invalid"

    print("\n-- Done --")

start()

