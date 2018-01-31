#!/usr/bin/env python
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup


from llabs.utils.gdocs import GoogleDoc

TEST_URL = 'https://docs.google.com/document/d/1o6dsEyaauj3wc5HwZsvrWIFVE4Uw3sr3vODQQpJmbe4/edit?usp=sharing'
TEST_URL_IMG = 'https://docs.google.com/document/d/1lQSRiRCjJ1y5P7jNDSLj70Ci6e_cSZYj2VLaMeqxw_o/edit?usp=sharing'


def test_init():
    """ Test initialization """
    doc = GoogleDoc(TEST_URL)
    assert doc.url == TEST_URL


def test_clean_header_tag():
    """ pytest test_gdocs.py::test_clean_header_tag """
    doc = GoogleDoc(TEST_URL_IMG)
    soup = BeautifulSoup(doc.html, 'html.parser')
    html = ''
    for tag in soup('h2'):
        html += GoogleDoc.clean_header_tag(tag)
    expected = u"""<h2>Don’t Book Your Room Above The Party Room</h2><h2>Holland America Is Great</h2><h2>A Cruise Is A Great Forced Break From The Internet</h2>"""
    assert html == expected
