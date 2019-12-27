import sys, time, os, copy

from components import navigable_menus, arxiv_api

@navigable_menus.nav_stack
def search(NAVSTACK, STATE):
    navigable_menus.make_header('main >> search')
    search_results, STATE = arxiv_api.search(STATE)
    if search_results == []:
        navigable_menus.error('no results found or query empty')
        return ('main_menu', 'back'), NAVSTACK, STATE

    articles = navigable_menus.make_articles(search_results, sys.modules[__name__])
    articles = navigable_menus.paginate(
        articles, page_length=10,
        menu_options=[
            ('main_menu', 'back'),
            ('main_menu', 'back_to_main'),
            ('CONTROL', 'previous_page'),
            ('CONTROL', 'next_page')
        ]
    )
    action, STATE = navigable_menus.create(
        articles, header='main >> search',
        STATE=STATE
    )

    return action, NAVSTACK, STATE
