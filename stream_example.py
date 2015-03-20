#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Stream
~~~~~
"""

import tweepy
import utils
import config

auth = tweepy.OAuthHandler(config.consumer_key, config.consumer_secret)
auth.set_access_token(config.access_token, config.access_token_secret)

api = tweepy.API(auth)
keywords = config.keywords


class StreamListener(tweepy.StreamListener):
    def on_connect(self):
        print 'Streaming started...'

    def on_status(self, status):
        tweet = status.text.lower()

        # If one of the keywords is in the tweet then
        # TODO: Need to compare word by word in each list
        # http://bit.ly/19EBu0J
        if any(keyword in tweet for keyword in keywords):
            tweet_url = 'http://twitter.com/{0}/status/{1}'\
                          .format(status.author.screen_name,
                                  str(status.id))

            tweet = '{0} \n\r @{1} says: "{2}"'\
                    .format(tweet_url, status.user.screen_name, 
                            status.text.encode('utf-8'))
            print tweet

    def on_direct_message(self, status):
        print status
        return

    def on_exception(self, exception):
        print exception
        return False

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_data disconnects the stream
            return False

    def on_disconnect(self, notice):
        print 'Disconnected'
        return False

    def on_warning(self, notice):
        print notice
        return False


def main():
    listener = StreamListener()
    stream = tweepy.Stream(auth=api.auth, listener=listener)

    try:
        stream.filter(locations=[-95.62, 29.5, -94.83, 30.6], async=True)
    except:
        print 'Error'
        stream.disconnect()

if __name__ == '__main__':
    main()
