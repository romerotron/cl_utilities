#!/usr/bin/env python
# -*- coding: utf-8 -*-
from llabs.utils.gdocs import GoogleDoc

TEST_URL = 'https://docs.google.com/document/d/1uhTwOqMg37ENV6YcnzM45WQcjr7N9_RK98v_WD-brc0/edit?usp=sharing'


def test_init():
    """ Test initialization """
    doc = GoogleDoc(TEST_URL)
    assert doc.url == TEST_URL
