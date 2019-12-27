import sys, time, os, copy

from components import navigable_menus, arxiv_api
from ml import main_ml

@navigable_menus.nav_stack
def arxiv(NAVSTACK, STATE):
    action, STATE = navigable_menus.create(
        [
            ('arxiv', 'new_articles'),
            ('arxiv', 'recommended'),
            ('main_menu', 'back'),
            ('main_menu', 'back_to_main')
        ], header='main >> arxiv', STATE=STATE
    )
    return action, NAVSTACK, STATE


##########################################################################
# NEW ARTICLE MENUS

@navigable_menus.nav_stack
def new_articles(NAVSTACK, STATE):
    categories = [
        ('arxiv', 'new_cs'),
        ('arxiv', 'new_physics'),
        ('arxiv', 'new_q_bio'),
        ('arxiv', 'new_math'),
        ('arxiv', 'new_non_linear_math')
    ]

    action, STATE = navigable_menus.create(
        categories + [
            ('main_menu', 'back'),
            ('main_menu', 'back_to_main')
        ], header='main >> arxiv >> new articles', STATE=STATE
    )
    return action, NAVSTACK, STATE

@navigable_menus.nav_stack
def new_cs(NAVSTACK, STATE):
    try:
        feed_items, STATE = arxiv_api.get_feed(topic='cs', STATE=STATE)
    except:
        navigable_menus.error('request timed out. standby...')
        return ('main_menu', 'do_nothing'), NAVSTACK, STATE
    articles = navigable_menus.make_articles(feed_items, sys.modules[__name__])
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
        articles, header='main >> arxiv >> new articles >> cs',
        STATE=STATE
    )
    return action, NAVSTACK, STATE

@navigable_menus.nav_stack
def new_physics(NAVSTACK, STATE):
    try:
        feed_items, STATE = arxiv_api.get_feed(topic='physics', STATE=STATE)
    except:
        navigable_menus.error('request timed out. standby...')
    articles = navigable_menus.make_articles(feed_items, sys.modules[__name__])
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
        articles, header='main >> arxiv >> new articles >> physics',
        STATE=STATE
    )

    return action, NAVSTACK, STATE

@navigable_menus.nav_stack
def new_q_bio(NAVSTACK, STATE):
    try:
        feed_items, STATE = arxiv_api.get_feed(topic='q-bio', STATE=STATE)
    except:
        navigable_menus.error('request timed out. standby...')
    articles = navigable_menus.make_articles(feed_items, sys.modules[__name__])
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
        articles, header='main >> arxiv >> new articles >> quantum biology',
        STATE=STATE
    )

    return action, NAVSTACK, STATE

@navigable_menus.nav_stack
def new_math(NAVSTACK, STATE):
    try:
        feed_items, STATE = arxiv_api.get_feed(topic='math', STATE=STATE)
    except:
        navigable_menus.error('request timed out. standby...')
    articles = navigable_menus.make_articles(feed_items, sys.modules[__name__])
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
        articles, header='main >> arxiv >> new articles >> math',
        STATE=STATE
    )

    return action, NAVSTACK, STATE

@navigable_menus.nav_stack
def new_non_linear_math(NAVSTACK, STATE):
    try:
        feed_items, STATE = arxiv_api.get_feed(topic='nlin', STATE=STATE)
    except:
        navigable_menus.error('request timed out. standby...')
    articles = navigable_menus.make_articles(feed_items, sys.modules[__name__])
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
        articles, header='main >> arxiv >> new articles >> non-linear math',
        STATE=STATE
    )

    return action, NAVSTACK, STATE



##########################################################################



@navigable_menus.nav_stack
def recommended(NAVSTACK, STATE):
    categories = [
        ('arxiv', 'recommended_cs'),
        ('arxiv', 'recommended_physics'),
        ('arxiv', 'recommended_q_bio'),
        ('arxiv', 'recommended_math'),
        ('arxiv', 'recommended_non_linear_math')
    ]

    action, STATE = navigable_menus.create(
        categories + [
            ('main_menu', 'back'),
            ('main_menu', 'back_to_main')
        ], header='main >> arxiv >> recommended', STATE=STATE
    )
    return action, NAVSTACK, STATE

@navigable_menus.nav_stack
def recommended_cs(NAVSTACK, STATE):
    try:
        feed_items, STATE = arxiv_api.get_feed(topic='cs', STATE=STATE)
        print('-'*80)
        print('generating recommendations. standby...')
        feed_items, STATE = main_ml.predict(feed_items, STATE=STATE)
    except:
        navigable_menus.error(
            'request timed out or prediction algorithms have failed. standby...'
        )
    articles = navigable_menus.make_articles(feed_items, sys.modules[__name__])
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
        articles, header='main >> arxiv >> recommended >> cs',
        STATE=STATE
    )

    return action, NAVSTACK, STATE

@navigable_menus.nav_stack
def recommended_physics(NAVSTACK, STATE):
    try:
        feed_items, STATE = arxiv_api.get_feed(topic='physics', STATE=STATE)
        print('-'*80)
        print('generating recommendations. standby...')
        feed_items, STATE = main_ml.predict(feed_items, STATE=STATE)
    except:
        navigable_menus.error(
            'request timed out or prediction algorithms have failed. standby...'
        )
    articles = navigable_menus.make_articles(feed_items, sys.modules[__name__])
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
        articles, header='main >> arxiv >> recommended >> physics',
        STATE=STATE
    )

    return action, NAVSTACK, STATE

@navigable_menus.nav_stack
def recommended_q_bio(NAVSTACK, STATE):
    try:
        feed_items, STATE = arxiv_api.get_feed(topic='q-bio', STATE=STATE)
        print('-'*80)
        print('generating recommendations. standby...')
        feed_items, STATE = main_ml.predict(feed_items, STATE=STATE)
    except:
        navigable_menus.error(
            'request timed out or prediction algorithms have failed. standby...'
        )
    articles = navigable_menus.make_articles(feed_items, sys.modules[__name__])
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
        articles, header='main >> arxiv >> recommended >> quantum biology',
        STATE=STATE
    )

    return action, NAVSTACK, STATE

@navigable_menus.nav_stack
def recommended_math(NAVSTACK, STATE):
    try:
        feed_items, STATE = arxiv_api.get_feed(topic='math', STATE=STATE)
        print('-'*80)
        print('generating recommendations. standby...')
        feed_items, STATE = main_ml.predict(feed_items, STATE=STATE)
    except:
        navigable_menus.error(
            'request timed out or prediction algorithms have failed. standby...'
        )
    articles = navigable_menus.make_articles(feed_items, sys.modules[__name__])
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
        articles, header='main >> arxiv >> recommended >> math',
        STATE=STATE
    )

    return action, NAVSTACK, STATE

@navigable_menus.nav_stack
def recommended_non_linear_math(NAVSTACK, STATE):
    try:
        feed_items, STATE = arxiv_api.get_feed(topic='nlin', STATE=STATE)
        print('-'*80)
        print('generating recommendations. standby...')
        feed_items, STATE = main_ml.predict(feed_items, STATE=STATE)
    except:
        navigable_menus.error(
            'request timed out or prediction algorithms have failed. standby...'
        )
    articles = navigable_menus.make_articles(feed_items, sys.modules[__name__])
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
        articles, header='main >> arxiv >> recommended >> non-linear math',
        STATE=STATE
    )

    return action, NAVSTACK, STATE
