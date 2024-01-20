#!/usr/bin/env python
# apis/sitemap_register.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"


def register_generator():
    yield 'main.index_page', {}
    yield 'main.portfolio_page', {}
    yield 'main.cv_page', {}
    yield 'main.contact_page', {}
    yield 'file.file_page', {}
    yield 'game.game_page', {}
