import os

from .base import *

DEBUG = os.getenv("DEBUG",False)

ALLOWED_HOSTS = [
    "youtube.impropy.me",
    "www.youtube.impropy.me",
    os.getenv('IP'),
]

