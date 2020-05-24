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

import math

from . import navigable_menus

def make_article(feed_item, module):
    """
    creates a single article route and returns the route name
    feed item must be an instance of feed.Feed
    """
    @navigable_menus.nav_stack
    def func(NAVSTACK, STATE):
        STATE.current_article = feed_item
        action, STATE = navigable_menus.create(
            [
                ('main_menu', 'download'),
                ('main_menu', 'back')
            ],
            header=feed_item.title(),
            before_content=feed_item.view(),
            STATE=STATE
        )
        return action, NAVSTACK, STATE

    # i sincerely hope this doesn't break at some point
    assert 'score' in feed_item.__dict__
    func.__name__ = f"_({feed_item.score}) {feed_item.title()}"
    setattr(module, func.__name__, func)
    return func.__name__

def make(feed_items, module):
    """
    create a list of article routes for display in menus in the form (module_name, article_name)
    """
    module_name = module.__name__.split('.')[-1]
    return [
        (module_name, name) for name in [make_article(item, module) for item in feed_items]
    ]

def paginate(articles=[], page_length=0, menu_options=[]):
    """
    pagination mechanism for a list of articles
    """
    max_page = math.ceil(len(articles) / page_length)
    if max_page == 0: max_page = 1
    return [articles[page*page_length:(page+1)*page_length]+menu_options for page in range(max_page)]
