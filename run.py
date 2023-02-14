#!/usr/bin/env python
# run.py
__author__ = "lavandejoey, Ziyi LIU"
__copyright__ = "Copyright 2021-2023"
__license__ = ""
__version__ = "0.0.1"
__maintainer__ = "lavandejoey"
__email__ = "lavandejoey@outlook.com"

# standard library
import os

# 3rd party packages
# local source
from app import create_app

app = create_app()


def run():
    debug = os.environ.get("APP_DEBUG", True)
    host = os.environ.get("APP_HOST", "localhost")
    port = os.environ.get("APP_PORT", 8000)

    app.run(debug=debug, host=host, port=port)


if __name__ == '__main__':
    run()
