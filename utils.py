#!/usr/bin/env python

"""
utils
~~~~~

Tools I need for:
    - Scrapping
    - Create Twitter bots
"""

import config
import urllib
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

handler = logging.FileHandler(config.log_path)
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - '
                              '%(levelname)s - %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)

def send_email(from_, to, subject, msg):
    """
    Send an email using the mailgun API.

    Keyword arguments:
      from -- email sending the email
      to -- email that will receive the email
      subject -- email subject
      msg -- email msg
    """
    key = config.mailgun_key
    sandbox = config.mailgun_sandbox

    req_url = 'https://api.mailgun.net/v2/{0}/messages'\
              .format(sandbox)
    data = {'from':from_, 'to':to, 'subject':subject,
            'text':msg}

    r = requests.post(req_url, auth=('api', key), data=data)

    print 'Status: {0}'.format(r.status_code)
    print 'Body: {0}'.format(r.text)

def short_link(long_url):
    """
    Create a short link using the Bitly API from a
    given URL.

    Keyword arguments:
      long_url -- the URL that need to be shortened
      token -- Bitly API token
      api_url -- Bitly API URL
    """
    token = config.bitly_api_access_token
    api_url = config.bitly_api_url
    query_args = urllib.urlencode({'access_token': token,
                                   'longUrl': long_url})
    query_url = '{0}?{1}'.format(api_url, query_args)
    request = requests.get(query_url)
    status_code = request.json()['status_code']

    if status_code == 403:
        return
    elif status_code == 500:
        return long_url
    else:
        link = request.json()['data']['link_save']['link']
        if status_code == 304:
            return link
        else:
            return link

def uniquify(list_one, list_two):
    """
    Return a list from a combination of two omiting
    repeated values.

    $ print uniquify([0, 1, 2, 3], [9, 8, 7, 5, 1, 0])
    >> [0, 1, 2, 3, 4, 5, 7, 8, 9]
    """
    return list(set(list_one) - set(list_two))

def has_badword(text, badwords_file):
    """Return `True` if a badword is in a phrase."""
    # Create a list of words and remove ":" on the fly.
    words = [x.replace(':', '') for x in text.split(' ')]

    f = open(badwords_file, 'r')
    lines = f.readlines()
    f.close()

    # Check if a *badword* is in the `words` list.
    return True in map(lambda l: l.strip() in words, lines)

def hashtag_words(text):
    """
    Compare words in the string with the `keywords.txt`
    file and if it find one match, it will convert it to
    a hashtag.
    """
    text = text.split(' ')

    f = open(config.keywords_file, 'r')
    keywords = f.readlines()
    f.close()

    for index, word in enumerate(text):
        for keyword in keywords:
            if word.lower().strip() == keyword.lower().strip():
                text[index] = '#' + str(keyword).strip()

    return (' ').join(text)

def compose_tweet(long_text, url):
    """Return a string of 140 chars from a long text given
    creating a 'Tweet' with it.

    Keyword arguments:
      long_text -- Text that need to be short
      url -- URL that need to go along with the tweet
    """
    letters = []

    # Clean long_text from white-spaces
    long_text = long_text.split(' ')

    for line in long_text:
        if len((' ').join(letters)) <= 106:
            letters.append(line)
        else:
            letters[-1] = '...'
            break

    tweet = ((' ').join(letters)).strip('\r\n') + ' - ' + url
    logger.info('Composing tweet: ' + str(tweet.encode('utf-8')))

    return tweet.encode('utf-8')
