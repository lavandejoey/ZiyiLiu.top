#!/usr/bin/env python
# run.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = ""
__email__ = "lavandejoey@outlook.com"

# standard library
import os

# 3rd party packages
# local source
from MainApplication import create_main_app

MainApp = create_main_app()

debug = os.environ.get("APP_DEBUG", True)
host = os.environ.get("APP_HOST", "127.0.0.1")
port = os.environ.get("APP_PORT", 8000)
MainApp.run(debug=debug, host=host, port=port)
