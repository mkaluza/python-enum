#! /usr/bin/env python

from distutils.core import setup, Extension

import sys

_ext_modules = None

setup(
    name = "enum",
    version = "0.1",
    description = "Python enum class",
    author = "Marcin Kaluza",
    author_email = "mk@flex.pm",
    url = "http://github.com/mkaluza/python-enum/",
    
    packages = [
	    "enum",
        ],

    ext_modules = _ext_modules
)

