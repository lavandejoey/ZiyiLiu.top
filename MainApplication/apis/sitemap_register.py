#!/usr/bin/env python
# apis/sitemap_register.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = "Apache 2.0"
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

from MainApplication.extentions import sitemap


@sitemap.register_generator
def register_generator():
    yield 'main.index_page', {}
    yield 'main.portfolio_page', {}
    yield 'main.cv_page', {}
    yield 'main.contact_page', {}
    yield 'main.directory_page', {}
    yield 'auth.login_page', {}
    yield 'auth.signup_page', {}
    yield 'auth.logout_page', {}
    yield 'ip.set_client_locale', {"language": "en"}
    yield 'ip.set_client_locale', {"language": "zh_Hans"}
    yield 'ip.set_client_locale', {"language": "zh_Hant"}
    yield 'ip.set_client_locale', {"language": "yue"}
    yield 'ip.set_client_locale', {"language": "fr"}
