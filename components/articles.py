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
    func.__name__ = f"_{feed_item.title()}"
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
