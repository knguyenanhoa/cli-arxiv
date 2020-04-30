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
