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
import logging

# 3rd party packages
# local source
from MainApplication import main_app

# Init console debug log "JoshuaZiyiLiu"
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logging.debug("Debug mode is on.")

# Create the main application
debug = os.environ.get("APP_DEBUG", True)
host = os.environ.get("APP_HOST", "127.0.0.1")
# host = os.environ.get("APP_HOST", "192.168.3.8")
port = os.environ.get("APP_PORT", 1211)
main_app.run(debug=debug, host=host, port=port)
