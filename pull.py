import json
from flask import Flask, request
from threading import Timer
from IPython.display import IFrame
from IPython.display import display
from IPython.display import Javascript as JS

import twitter
from twitter.oauth_dance import parse_oauth_tokens
from twitter.oauth import read_token_file, write_token_file

# XXX: Go to http://dev.twitter.com/apps/new to create an app and get values
# for these credentials, which you'll need to provide in place of these
# empty string values that are defined as placeholders.
# See https://dev.twitter.com/docs/auth/oauth for more information 
# on Twitter's OAuth implementation.

CONSUMER_KEY = 'fGQNvRO9UObcPc2rXk5ne24c4'
CONSUMER_SECRET = 'lw79cyT36k8RjR1vAHTnwIhQjQ2fg85BM1lCR8S7gyMKoLd6BE'
OAUTH_TOKEN = '921712020-w9OX1XNMLjcuunhWadaUrSFe0B69fCHutNs9w0Uw'
OAUTH_TOKEN_SECRET = 'fN9qw3Hq3Wf19Dy251JQFKRnayU9G2vpV62GuzLQqQWEX'

auth = twitter.oauth.OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET,
                           CONSUMER_KEY, CONSUMER_SECRET)

twitter_api = twitter.Twitter(auth=auth)

# Nothing to see by displaying twitter_api except that it's now a
# defined variable

print twitter_api

# Streaming API live pull of filtered tweets (by search term)

import twitter
import sys

# Query terms

q = 'ebola' # Comma-separated list of terms

print >> sys.stderr, 'Filtering the public timeline for track="%s"' % (q,)

# Reference the self.auth parameter
twitter_stream = twitter.TwitterStream(auth=twitter_api.auth)

# See https://dev.twitter.com/docs/streaming-apis
stream = twitter_stream.statuses.filter(track=q)

#Need a counter on the time / number tweets retrieved 

#Plus a counter to generate successive timestamp

#Set up database to write pulled tweets to

from pymongo import MongoClient
client = MongoClient()
db = client.ebodata
collection = db.rawdata_20141119

# Append each to db IF English language

for tweet in stream:
    if tweet['lang'] == 'en':
    	collection.insert(tweet)