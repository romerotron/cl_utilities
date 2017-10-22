#!/usr/bin/env python
# -*- coding: utf-8 -*-
from llabs.utils import craigslist


def test_fetch_rss_feed():
    """Test something."""
    url = 'https://sfbay.craigslist.org/search/tix?format=rss'
    doc, fetched, code = craigslist.fetch_rss_feed(url)
    assert fetched is True
