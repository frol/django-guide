#!/usr/bin/python

import os
from setuptools import setup, find_packages

from guide import VERSION, PROJECT


MODULE_NAME = 'django-guide'
PACKAGE_DATA = [
    'locale/ru/LC_MESSAGES/django.mo',
    'locale/ru/LC_MESSAGES/django.po',
]


def read( fname ):
    try:
        return open( os.path.join( os.path.dirname( __file__ ), fname ) ).read()
    except IOError:
        return ''


META_DATA = dict(
    name = PROJECT,
    version = VERSION,
    description = "Django module wrapper around jQuery-guides",
    long_description = read('README.rst'),
    license='GNU LGPL',

    author = "Vlad Frolov & Ilya Polosukhin",
    author_email = "frolvlad@gmail.com, ilblackdragon@gmail.com",

    url = "https://github.com/frol/django-guide.git",

    packages = find_packages(),
    package_data = { '': PACKAGE_DATA, },

    install_requires = [ 'django>=1.2' ],
)

if __name__ == "__main__":
    setup( **META_DATA )
