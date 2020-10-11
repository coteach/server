# coding:utf-8

import os
import re
import sys
import locale
from datetime import datetime
import requests

# info
DEVELOPMENT = False
__version__ = 0.1
PROJECT_NAME = "scraper"

# path
RETRY_CNT = 10
RETRY_DELAY = 10

# File Name
now = datetime.now().strftime("%Y%m%d_%H%M%S")
LOG_FILE_NAME = "./logs/" + now + ".log"
