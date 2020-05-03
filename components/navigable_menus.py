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

import os, copy, sys, termios, time, math, re

def make_header(text=' '):
    os.system('clear')
    print(text.upper())
    print('-'*80)

def error(text=' '):
    make_header('error')
    print(text)
    time.sleep(1)

def getch():
    """
    get char (blocking)
    adapted from code due to mevans
    https://stackoverflow.com/questions/13207678/whats-the-simplest-way-of-detecting-keyboard-input-in-python-from-the-terminal
    """

    fd = sys.stdin.fileno()

    oldterm = termios.tcgetattr(fd)
    newattr = termios.tcgetattr(fd)
    newattr[3] = newattr[3] & ~termios.ICANON & ~termios.ECHO
    termios.tcsetattr(fd, termios.TCSANOW, newattr)

    c = None

    try:
        c = sys.stdin.read(1)
    except IOError: pass
    termios.tcsetattr(fd, termios.TCSAFLUSH, oldterm)
    return c

def terminate():
    os.system('clear')
    make_header('goodbye')
    time.sleep(1)
    os.system('clear')
    sys.exit()

def before_and_after_content(before_content=None, after_content=None):
    def wrapper(content):
        def wrapped_content(*args, **kw):
            if before_content != None: print(before_content.upper())
            result = content(*args, **kw)
            if after_content != None: print(after_content.upper())
            return result
        return wrapped_content
    return wrapper

#TODO: refactor this
def create(
    menu_options,
    header=' ', page=0, STATE=None,
    before_content=None,
    after_content=None):

    @before_and_after_content(before_content, after_content)
    def main_content(idx):
        if menu_options[0].__class__.__name__ == 'list':
            options = copy.copy(menu_options[page])
        else:
            options = copy.copy(menu_options)
        if len(options)-1 < idx: idx = len(options)-1

        display_options = [action for route, action in options]
        display_options = [
            '>> '+o if i == idx else '   '+o for i, o in enumerate(display_options)
        ]
        [print(x) for x in display_options]

        return options


    if STATE == None or STATE.__class__.__name__ != 'Store':
        raise Exception('you must provide STATE of type Store')
    if STATE.curr_page != []: page = STATE.curr_page
    idx = STATE.curr_idx if STATE.curr_idx != [] else 0

    while True:
        make_header(header)
        options = main_content(idx)
        c = getch()

        # a bit of vim never hurt anyone
        if c == 'k': idx = (idx - 1) % len(options)
        if c == 'j': idx = (idx + 1) % len(options)
        if c == 'G' or c == 'J': idx = len(options) - 1
        if c == 'K': idx = 0
        if c == 'g':
            c = getch()
            if c == 'g': idx = 0
        if c == '\n' or c == 'o': # submit choice
            try:
                if options[idx] == ('CONTROL', 'previous_page'):
                    page = (page - 1) % len(menu_options)
                elif options[idx] == ('CONTROL', 'next_page'):
                    page = (page + 1) % len(menu_options)
                elif options[idx] == ('main_menu', 'back'):
                    #don't do any cursor calculation, just go back
                    return ('main_menu', 'back'), STATE
                else:
                    STATE.curr_page = page
                    STATE.curr_idx = idx
                    return options[idx], STATE
            except:
                return options[-1], STATE
        if c == 'q': return ('main_menu', 'back'), STATE
        if c == 'd': return ('main_menu', 'download'), STATE
        if c == '\x1b': # escape char
            terminate()

def nav_stack(func):
    """
    decorator to increment navigation stack.
    must decorate most menu routes if these implement the back function
    """
    def new_func(s, st):
        a, _, _ = func(s, st)
        s += [a]
        return a, s, st
    return new_func

def make_article(feed_item, module):
    """
    creates a single article route and returns the route name
    feed item must be an instance of feed.Feed
    """
    @nav_stack
    def func(NAVSTACK, STATE):
        STATE.current_article = feed_item
        action, STATE = create(
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
    func.__name__ = f"_{feed_item.title()}"
    setattr(module, func.__name__, func)
    return func.__name__

def make_articles(feed_items, module):
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
