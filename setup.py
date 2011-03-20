#!/usr/bin/env python
from setuptools import setup, find_packages

setup(
    name="cony",
    version="0.2.1",
    description=(
        '"Cony" is a tool to write smart bookmarks in '
        'python and to share them across all your browsers and with a '
        'group of people or the whole world. This project inspired '
        'by Facebook\'s bunny1.'
    ),
    keywords='bottle webapp smart bookmark browser',
    license = 'New BSD License',
    author="Alexander Artemenko",
    author_email='svetlyak.40wt@gmail.com',
    url='http://dev.svetlyak.ru/cony/',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: BSD License',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Server',
    ],
    packages=find_packages(),
    scripts=['cony-server'],
    install_requires = ['bottle'],
)
