# coding=utf-8
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup
import githon

requirements = open('requirements.pip').read().splitlines()

kw = dict(
    name = 'githon',
    version = '0.5.7',
    description = 'A simple Data Scraping library for GitHub REST API v3',
    long_description = open('README.md', 'r').read(),
    author = 'Marcos Vinícius Brás',
    author_email = 'marcosvbras@gmail.com',
    url = 'https://github.com/marcosvbras/githon',
    download_url = 'https://github.com/marcosvbras/githon',
    license='Apache',
    py_modules = ['githon'],
    packages=['githon'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords='data github scraping api',
    install_requires=requirements,
    python_requires='~=3.3',
)

setup(**kw)
