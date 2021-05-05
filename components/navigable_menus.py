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
            try:
                options = copy.copy(menu_options[page])
            except:
                options = copy.copy(menu_options[0])
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
        if c == 'h': page = (page - 1) % len(options)
        if c == 'l': page = (page + 1) % len(options)
        if c == 'G' or c == 'J': idx = len(options) - 1
        if c == 'K': idx = 0
        if c == 'g':
            c = getch()
            if c == 'g': idx = 0
        if c in ['\n', 'o']: # submit choice
            try:
                if options[idx] == ('CONTROL', 'previous_page'):
                    page = (page - 1) % len(options)
                elif options[idx] == ('CONTROL', 'next_page'):
                    page = (page + 1) % len(options)
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

def nav_stack(menu_item):
    """
    decorator to support navigation stack.
    must decorate most menus if these implement the back function
    """
    def menu_item_with_nav_stack_support(stack, state):
        action, _, _ = menu_item(stack, state)
        stack += [action]
        return action, stack, state
    return menu_item_with_nav_stack_support

