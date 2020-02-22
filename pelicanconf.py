#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Anton Savill'
SITENAME = "Anton's Website"
SITEURL = 'anton.savill.id.au'

PATH = 'content'

TIMEZONE = 'Australia/Perth'

DEFAULT_LANG = 'English'
THEME = "./theme"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('My old, abandoned website', 'http://notna888.beevomit.org/'),
         # ('', '#'),
        )

# Social widget
SOCIAL = (('Twitter', 'https://twitter.com/notna888'),
          ('Github', 'https://github.com/notna888'),
          # ('', '#'),
         )

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True

PLUGINS = ['encrypt_content']


ENCRYPT_CONTENT = {
    'title_prefix': '[Encrypted]',
    'summary': 'This content is encrypted.'
}
