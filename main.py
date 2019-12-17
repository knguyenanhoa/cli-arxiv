import sys, os, time, copy
import requests

# THESE ARE USED, DO NOT REMOVE
# need to implement an autoloader here....
from menus import main_menu, arxiv, search

from components import navigable_menus, store

def route(action, NAVSTACK, STATE):
    action, NAVSTACK, STATE = getattr(
        globals()[action[0]],
        action[1]
    )(NAVSTACK, STATE)
    return action, NAVSTACK, STATE


if __name__ == '__main__':
    os.system('clear')
    navigable_menus.make_header('welcome to arXiv. initializing...')

    NAVSTACK = [('main_menu', 'main')]
    STATE = store.Store()

    os.system('clear')
    action, NAVSTACK, STATE = main_menu.main(NAVSTACK, STATE)

    while True:
        action, NAVSTACK, STATE = route(action, NAVSTACK, STATE)
