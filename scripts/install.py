#!/usr/bin/python

import os

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))
        )
src = os.path.join(__location__, '../src/main.py')
dst = '/usr/local/bin/surface'

os.symlink(src, dst)

print("Installation done")
