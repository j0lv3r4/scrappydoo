#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Scrape quotes from 
http://www.brainyquote.com/
"""

import requests
import time
from bs4 import BeautifulSoup
from random import randint
from fake_useragent import UserAgent

USER_AGENT =  UserAgent()
HEADERS = {'content-encoding': 'gzip', 'User-Agent': USER_AGENT.google}
URL = 'http://www.brainyquote.com/quotes/topics/'
TOPIC = 'topic_motivational'
FILE = './quotes_motivational.txt'
PAGES = range(0, 9)

def main():
    try:
        for page in PAGES:
            quotes = []
            random_number = randint(5, 15)
            num = '' if page == 0 else page
            url = '{0}{1}{2}.html'.format(URL, TOPIC, num)

            # Send request
            print 'sending request to {0}'.format(url) 
            r = requests.get(url, headers=HEADERS)
            html = BeautifulSoup(r.text)

            # Scrape data
            print 'Scrapping data.'
            html_quotes = html.find_all('div', class_='boxyPaddingBig')

            for html_quote in html_quotes:
                body = html_quote.find(attrs={'title': 'view quote'}).text
                author = html_quote.find(attrs={'title': 'view author'}).text
                quote = '{0} - {1} \n'.format(body, author)
                quotes.append(quote)

            # Read file
            print 'Reading file.'
            f = open(FILE, 'r')
            file_quotes = f.readlines()
            f.close()

            # Merge lists
            print 'Merging lists.'
            quotes = file_quotes + quotes

            # Write file
            print 'Writing file.'
            f = open(FILE, 'w')
            f.writelines(quotes)
            f.close()

            print 'Sleeping {0} seconds'.format(random_number)
            time.sleep(random_number)

    except KeyboardInterrupt:
        print 'Stopping scraper.'

if __name__ == '__main__':
    main()
