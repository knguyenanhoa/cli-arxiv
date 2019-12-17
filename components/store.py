class Store():
    """
    State store
    SET: object.attribute = data (any type)
    GET: object.attribute

    Each storage slot (attribute) will become stale after N GET ops
    N set on init (default 20)
    Stale count is reset on writing to the attribute
    """
    def __init__(self, stale_count=20):
        object.__setattr__(self, 'stale_threshold', stale_count)

    def __getattribute__(self, key):
        # this is to prevent inf recursion as
        # we're overriding __getattribute__
        if key in dir(object):
            return object.__getattribute__(self, key)

        if key == 'stale_threshold':
            raise AttributeError

        k = object.__getattribute__(self, key)['key']
        c = object.__getattribute__(self, key)['stale_count']
        sc = object.__getattribute__(self, 'stale_threshold')

        object.__setattr__(self, key, {'key': k, 'stale_count': c + 1})

        if object.__getattribute__(self, key)['stale_count'] > sc:
            object.__setattr__(self, key, {'key': [], 'stale_count': 0})

        return object.__getattribute__(self, key)['key']

    def __getattr__(self, key):
        if key == 'stale_threshold':
            raise AttributeError

        object.__setattr__(self, key, {'key': [], 'stale_count': 0})
        return object.__getattribute__(self, key)['key']

    def __setattr__(self, key, val):
        """
        implement safe store attr setter
        replacement assignment only
        writing to store resets stale count
        """
        object.__setattr__(self, key, {'key': val, 'stale_count': 0})

        #TODO: add something to inspect storage
