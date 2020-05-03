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

import sys, time, os, copy

from components import navigable_menus
from menus import main_menu

@navigable_menus.nav_stack
def man(NAVSTACK, STATE):
    navigable_menus.make_header('main >> help')
    print(' ')
    print('Navigation is vim-like')
    print('UP: k      DOWN: j      LEFT: h      RIGHT: l')
    print('BOTTOM: G, J            TOP: gg, K')
    print(' ')
    print('DOWNLOAD: d (where applicable)')
    print('SELECT:   o, enter')
    print('BACK:     q')
    print('EXIT:   esc (works on most screens)')
    print('-----------------------------------------------')
    print('Press any key to return')

    c = navigable_menus.getch()
    return main_menu.back(NAVSTACK, STATE)
