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
