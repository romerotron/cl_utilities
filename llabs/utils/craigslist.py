# -*- coding: utf-8 -*-

import logging

import feedparser
import requests


class Ad(object):
    """A Craigslist Ad object.
    
    Attributes:
        title: the title of the ad
        description: the description text of the ad
        url: the URL to the ad
    """


    def __init__(self, title, description, url):
        """Init and return an Ad object with, title, description, url""" 
        self.title = title 
        self.description = description
        self.url = url 
        

def convert_rss_item_to_ad(self, item, **kwargs):
    """ Converts a RSS item to a CL ad """
    return Ad(item.title, item.description, item.link) 


def fetch_rss_feed(feed_url):
    """Downloads a Craigslist RSS feed from a url.
    
    Args:
        doc: The content of an RSS document from Craigslist
    """
    try:
        r = requests.get(feed_url)
        if r.status_code != 200:
            return 'unable to crawl url', False, r.status_code

        return r.content, True, r.status_code
    except:
        logging.exception('')


def ads_from_feed_doc(doc):
       """ Returns a list of ads from a CL RSS document by parsing the feed
       and converting the RSS items to a CL Ad object.

       Args:
           doc: The content of an RSS document from Craigslist
       """
       d = feedparser.parse(self.doc)
   
       for i, item in enumerate(d.entries):
           if i > -1:
               ads.append(convert_rss_item_to_ad(item))

       return ads

