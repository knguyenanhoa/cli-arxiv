import sys, time, os, copy

from components import navigable_menus, arxiv_api

def back_to_main(NAVSTACK, STATE):
    NAVSTACK = [('main_menu', 'main')]
    return ('main_menu', 'main'), NAVSTACK, STATE

def back(NAVSTACK, STATE):
    try:
        NAVSTACK.pop() #pop back action
        NAVSTACK.pop() #pop current action
        return NAVSTACK[-1], NAVSTACK, STATE
    except:
        # pretty much do nothing - should already be at root node
        return ('main_menu', 'main'), NAVSTACK, STATE

def do_nothing(NAVSTACK, STATE):
    try:
        NAVSTACK.pop() #pop current action
        return NAVSTACK[-1], NAVSTACK, STATE
    except:
        # pretty much do nothing - should already at root node
        return ('main_menu', 'main'), NAVSTACK, STATE

def download(NAVSTACK, STATE):
    #downloads article in STATE.current_article
    if STATE.current_article != []:
        try:
            STATE.current_article.download()
        except:
            navigable_menus.error('request timed out. standby...')
        action, NAVSTACK, STATE = back(NAVSTACK, STATE)
    else:
        navigable_menus.error('not an article. standby...')
        action, NAVSTACK, STATE = do_nothing(NAVSTACK, STATE)

    STATE.current_article = []

    return action, NAVSTACK, STATE

@navigable_menus.nav_stack
def main(NAVSTACK, STATE):
    """
    create a new menu by:
        1. add to this menu e.g ('new', 'index')
        2. create a file under menus/ with the same name e.g. 'new'
        3. the file should contain 'index' as a function, implemented
           similarly to this index function. all other functions are
           implemented the same.
        4. NOTE that the function names will match those selectable
           in the menus
    """
    # refresh search results when back to main menu
    STATE.search_results = []

    action, STATE = navigable_menus.create(
        [
            ('arxiv', 'arxiv'),
            ('search', 'search'),
            ('man', 'man'),
        ], header='main', STATE=STATE
    )
    return action, NAVSTACK, STATE
