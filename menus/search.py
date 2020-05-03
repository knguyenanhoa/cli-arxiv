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

from components import navigable_menus, arxiv_api, articles

@navigable_menus.nav_stack
def search(NAVSTACK, STATE):
    navigable_menus.make_header('main >> search')
    search_results, STATE = arxiv_api.search(STATE)
    if search_results == []:
        navigable_menus.error('no results found or query empty')
        return ('main_menu', 'back'), NAVSTACK, STATE

    ar = articles.make(search_results, sys.modules[__name__])
    ar = articles.paginate(
        ar, page_length=10,
        menu_options=[
            ('main_menu', 'back'),
            ('main_menu', 'back_to_main'),
            ('CONTROL', 'previous_page'),
            ('CONTROL', 'next_page')
        ]
    )
    action, STATE = navigable_menus.create(
        ar, header='main >> search',
        STATE=STATE
    )

    return action, NAVSTACK, STATE
