import unittest

from friend import collections


class CollectionsTests(unittest.TestCase):
    def test_select_dict(self):
        dicts = [
            {'a': 'A', 'b': 'B', 'c': 'C'},
            {'one': 'won'},
            {'one': 1, 'two': 2},
        ]
        expectations = (
            (
                'one',
                'won',
                [{'one': 'won'}]
            ),
            (
                'one',
                ('won', 1),
                [{'one': 'won'}, {'one': 1, 'two': 2}]
            ),
            (
                'one',
                (2, 'won'),
                [{'one': 'won'}]
            ),
            (
                2,
                0,
                []
            ),
            (
                'a',
                'B',
                []
            ),
            (
                'a',
                'A',
                [{'a': 'A', 'b': 'B', 'c': 'C'}]
            ),
            (
                0,
                (),
                []
            )
        )
        for key, value, d in expectations:
            self.assertEquals(collections.select_dict(dicts, key, value), d)
