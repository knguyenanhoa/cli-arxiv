import sys, time, os, copy

from components import navigable_menus
from menus import main_menu

@navigable_menus.nav_stack
def man(NAVSTACK, STATE):
    navigable_menus.make_header('main >> help')
    print(' ')
    print('Navigation is vim-like')
    print('UP: k      DOWN: j      LEFT: j      RIGHT: l')
    print('BOTTOM: G  TOP: Gj')
    print(' ')
    print('DOWNLOAD: d (where applicable)')
    print('SELECT:   o, enter')
    print('BACK:     q')
    print('EXIT:   esc (works on most screens)')
    print('-----------------------------------------------')
    print('Press any key to return')

    c = navigable_menus.getch()
    return main_menu.back(NAVSTACK, STATE)
