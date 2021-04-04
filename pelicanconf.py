#!/usr/bin/env python
# -*- coding: utf-8 -*- #

AUTHOR = 'Ross'
SITENAME = 'RossW.co.uk'
SITEURL = 'https://rossw.co.uk'

PATH = 'content'

TIMEZONE = 'Europe/London'

DEFAULT_LANG = 'en'

STATIC_PATHS =(('images'),)

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'https://getpelican.com/'),
         ('Python.org', 'https://www.python.org/'),
         ('Jinja2', 'https://palletsprojects.com/p/jinja/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 5

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True

FEED_DOMAIN = SITEURL
FEED_ALL_RSS = 'feeds/all.rss.xml'

THEME = 'rossw-blog-blue-penguin'

GITHUB_URL = "https://github.com/rosswf"
TWITTER_URL = "https://twitter.com/rossw_"

SITESUBTITLE = "Programming, DevOps, Homelabs & more"

# provided as examples, they make ‘clean’ urls. used by MENU_INTERNAL_PAGES.
TAGS_URL           = 'tag'
TAGS_SAVE_AS       = 'tag/index.html'
AUTHORS_URL        = 'author'
AUTHORS_SAVE_AS    = 'author/index.html'
CATEGORIES_URL     = 'category'
CATEGORIES_SAVE_AS = 'category/index.html'
ARCHIVES_URL       = 'archive'
ARCHIVES_SAVE_AS   = 'archive/index.html'

MENU_INTERNAL_PAGES = (
    # ('Categories', CATEGORIES_URL, CATEGORIES_SAVE_AS),
    ('Archives', ARCHIVES_URL, ARCHIVES_SAVE_AS),
)

PAGINATION_PATTERNS = (
    (1, '{url}', '{save_as}'),
    (2, '{base_name}/page/{number}/', '{base_name}/page/{number}/index.html'),
)