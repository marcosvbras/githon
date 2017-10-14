from distutils.core import setup
import sys

import githon

kw = dict(
    name = 'githon',
    version = githon.__version__,
    description = 'A simple Data Scraping library for GitHub REST API v3',
    long_description = open('README', 'r').read(),
    author = 'Marcos Vinícius Brás',
    author_email = 'marcosvbras@gmail.com',
    url = 'https://github.com/marcosvbras/githon',
    download_url = 'https://github.com/marcosvbras/githon',
    py_modules = ['githon'],
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ])

setup(**kw)
