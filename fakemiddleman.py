#!/usr/bin/env python

import time
import re
import random
import tweepy

random.seed()

CONSUMER_KEY = ""
CONSUMER_SECRET = ""
TOKEN_KEY = ''
TOKEN_SECRET = ''

MIN_WAIT = 60 # In minutes
MAX_WAIT = 6 * 60
MIDDLEMAN_FOLLOWERS = []
SPAMMERS = 0
MIDDLEMAN_TWEETS = open("middleman.txt").readlines()

def get_name(api):
    global MIDDLEMAN_FOLLOWERS, SPAMMERS
    num_followers = api.me().followers_count
    if num_followers != (len(MIDDLEMAN_FOLLOWERS) + SPAMMERS):
        MIDDLEMAN_FOLLOWERS = []
        SPAMMERS = 0
        for f in api.followers():
            # Basic spammer filter need a better than 1:4 follow ratio
            if float(f.followers_count / f.friends_count) > 0.25:
                MIDDLEMAN_FOLLOWERS.append(f.screen_name)
            else:
                SPAMMERS += 1
    if len(MIDDLEMAN_FOLLOWERS) == 0:
        return "Dubbie"
    return random.choice(MIDDLEMAN_FOLLOWERS)

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(TOKEN_KEY, TOKEN_SECRET)
api = tweepy.API(auth)

while (True):
    try:
        post = random.choice(MIDDLEMAN_TWEETS).strip()
        name = get_name(api)
        post = post.replace('{$NAME}', "@%s" % name)
        print post, name, len(MIDDLEMAN_TWEETS), SPAMMERS
        api.update_status(post)
        print "success"
    except Exception as e:
        print e
        pass
    sleepinterval = random.randrange(MIN_WAIT, MAX_WAIT)
    print "Sleeping for %d minutes" % sleepinterval 
    time.sleep(60 * sleepinterval)
