"""
ArXiv CLI Browser - a command line interface browser for the popular pre-print
academic paper website https://arxiv.org

Copyright (C) 2020  Klinkesorn Nguyen An Hoa

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License along
with this program; if not, write to the Free Software Foundation, Inc.,
51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.

Author contactable at k<dot>nguyen<dot>an<dot>hoa<at>gmail<dot>com
"""


import sys, os, copy

# THESE ARE USED, DO NOT REMOVE
# maybe implement an autoloader here....
from menus import main_menu, arxiv, search, man
from components import navigable_menus, store


def route(action, NAVSTACK, STATE):
    action, NAVSTACK, STATE = getattr(
        globals()[action[0]],
        action[1]
    )(NAVSTACK, STATE)
    return action, NAVSTACK, STATE

def init():
    try:
        os.mkdir("./data")
        os.mkdir("./data/summary")
        os.mkdir("./data/pdf")
        os.mkdir("./data/txt")
        os.mkdir("./to-read") #put things to read in here
    except:
        pass

    #check dependencies
    try:
        import requests, atoma
        from pdfminer.high_level import extract_text
        from sklearn.feature_extraction.text import TfidfVectorizer
        import numpy as np
    except:
        print('dependencies not satisfied')


if __name__ == '__main__':
    init()

    os.system('clear')
    navigable_menus.make_header('welcome to arXiv. initializing...')

    NAVSTACK = [('main_menu', 'main')]
    STATE = store.Store()

    os.system('clear')
    action, NAVSTACK, STATE = main_menu.main(NAVSTACK, STATE)

    while True:
        action, NAVSTACK, STATE = route(action, NAVSTACK, STATE)
