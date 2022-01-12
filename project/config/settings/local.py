import os

from .base import *

DEBUG = os.getenv("DEBUG",True)
ALLOWED_HOSTS = ["*"]
