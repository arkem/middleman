#!/usr/bin/env python

import twitter
import time
import re
import random

random.seed()

MIN_WAIT = 60 # In minutes
MAX_WAIT = 6 * 60
MIDDLEMAN_FOLLOWERS = []
SPAMMERS = 0
MIDDLEMAN_TWEETS = open("middleman.txt").readlines()

def get_name(api):
    global MIDDLEMAN_FOLLOWERS, SPAMMERS
    num_followers = api.users.show(screen_name = 'fakemiddleman')
    if num_followers != (len(MIDDLEMAN_FOLLOWERS) + SPAMMERS):
        MIDDLEMAN_FOLLOWERS = []
        SPAMMERS = 0
        next_cursor = -1
        while next_cursor != 0:
            res = api.statuses.followers(screen_name='fakemiddleman',\
                                         cursor=next_cursor)
            for u in res['users']:
                # Basic spammer filter need a better than 1:4 follow ratio
                if float(u['followers_count']) / u['friends_count'] > 0.25:
                    MIDDLEMAN_FOLLOWERS.append(u['screen_name'])
                else:
                    SPAMMERS += 1
            next_cursor = res['next_cursor']
            print next_cursor, type(next_cursor)
    if len(MIDDLEMAN_FOLLOWERS) == 0:
        return "Dubbie"
    return random.choice(MIDDLEMAN_FOLLOWERS)
    

while (True):
    try:
        post = random.choice(MIDDLEMAN_TWEETS).strip()
        api = twitter.Twitter("fakemiddleman", "crooked0little0vein")
        name = get_name(api)
        post = post.replace('{$NAME}', "@%s" % name)
        print post, name, len(MIDDLEMAN_TWEETS), SPAMMERS
        api.statuses.update(status = post)
        print "success"
    except Exception:
        pass
    sleepinterval = random.randrange(MIN_WAIT, MAX_WAIT)
    print "Sleeping for %d minutes" % sleepinterval 
    time.sleep(60 * sleepinterval)
