import requests
import sys
import os
import json
import pprint
import re
import urllib
import time
import socket

socket.setdefaulttimeout(10)

bingkey = "BINGKEYHERE"

# get tweet hashtag searchterm
args = sys.argv
search_hash = args[1]

# storage directory
store_base_path = "./images/"

# are we busy?
twittulatoring = False

def ensure_dir(f):
  d = os.path.dirname(f)
  if not os.path.exists(d):
      os.makedirs(d)


def twittulate():

  twittulatoring = True

  pp = pprint.PrettyPrinter(indent=0)

  r = requests.get('http://search.twitter.com/search.json?q=%23'+search_hash+'&rpp=1&include_entities=true&result_type=recent')

  result = json.loads(r.text)
  tweets = result['results']

  for tweet in tweets:

    # remove hashtag from tweet
    tweet_clean = re.sub(r'\s+',' ',re.sub(r'#\S+','',tweet['text']))

    # the path to store the images
    store_path = store_base_path + urllib.quote_plus(str(tweet_clean.encode("utf-8"))) + "/"
    
    # only store if tweet was not yet stored
    if not os.path.exists(store_path):

      # make sure path exists
      ensure_dir(store_path)

      print "\n------------------\nfound tweet: "+tweet['text']
      
      # use only first word
      search_term = urllib.quote(tweet_clean.split()[0]) # replace withsomething better?

      # use full tweet - hashtag
      # search_term = urllib.quote(tweet_clean)

      try:
        im_r = requests.get('http://api.bing.net/json.aspx?adultoption=off&Appid='+bingkey+'&query='+search_term+'&sources=image')
        im_result = json.loads(im_r.text)
        im_result = im_result['SearchResponse']['Image']['Results']

        print "found "+ str(len(im_result))+ " images\nfetching images:"

        for im in im_result:
          print im['MediaUrl']

          try:
            # retrieve and store images
            urllib.urlretrieve(im['MediaUrl'],store_path+os.path.basename(im['MediaUrl']))
          
          except(KeyboardInterrupt):
            print "OKAY I WILL QUIT."
            exit(0)
          except:
            print "fetch image messed up"

        print "------------------"

      except(KeyboardInterrupt):
        print "OKAY I WILL QUIT."
        exit(0)

      except:
        print "bing messed up"   

    else:

      print "found existing tweet:"+tweet['text']

  # DONE!
  twittulatoring = False

if __name__ == "__main__":
  
  while(True):
    if not twittulatoring:
      twittulate()

    time.sleep(10)