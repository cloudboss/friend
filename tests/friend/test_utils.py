import random
import unittest

import mock

from friend import strings
from friend import utils


class UtilsTests(unittest.TestCase):
    def test_retry_ex_no_failures(self):
        state = [0]
        ret = strings.random_alphanum(20)

        def wont_fail():
            if state[0] is None:
                state[0] += 1
                raise RuntimeError('Uh oh!')
            return ret

        self.assertEqual(utils.retry_ex(wont_fail), ret)
        self.assertEqual(state[0], 0)

    def test_retry_ex_single_retry(self):
        state = [0]
        ret = strings.random_alphanum(20)

        def will_recover_once():
            if state[0] == 0:
                state[0] += 1
                raise RuntimeError('Uh oh!')
            return ret

        self.assertEqual(utils.retry_ex(will_recover_once), ret)
        self.assertEqual(state[0], 1)

    def test_retry_ex_multiple_retries(self):
        state = [0]
        ret = strings.random_alphanum(20)
        count = random.randint(1, 6)

        def will_recover_count_times():
            if state[0] < count:
                state[0] += 1
                raise RuntimeError('Uh oh!')
            return ret

        self.assertEqual(
            utils.retry_ex(will_recover_count_times, times=count), ret
        )
        self.assertEqual(state[0], count)

    def test_retry_bool_no_failures(self):
        state = [0]

        def wont_fail():
            if state[0] is None:
                state[0] += 1
                return False
            return True

        self.assertEqual(utils.retry_bool(wont_fail), True)
        self.assertEqual(state[0], 0)

    def test_retry_bool_single_retry(self):
        state = [0]

        def will_recover_once():
            if state[0] == 0:
                state[0] += 1
                return False
            return True

        self.assertEqual(utils.retry_bool(will_recover_once), True)
        self.assertEqual(state[0], 1)

    def test_retry_bool_multiple_retries(self):
        state = [0]
        count = random.randint(1, 6)

        def will_recover_count_times():
            if state[0] < count:
                state[0] += 1
                return False
            return True

        self.assertEqual(
            utils.retry_bool(will_recover_count_times, times=count), True
        )
        self.assertEqual(state[0], count)

    def test_retry_ex_no_recover(self):
        state = [0]
        count = 5
        message = strings.random_alphanum(20)

        def wont_recover():
            if state[0] < count:
                state[0] += 1
                raise RuntimeError(message)
            return 'wont_return_this'

        with self.assertRaises(RuntimeError) as r:
            utils.retry_ex(wont_recover, times=count-1)
        self.assertEqual(r.exception.message, message)
        self.assertEqual(state[0], count)

    def test_retry_bool_no_recover(self):
        state = [0]
        count = 5

        def wont_recover():
            if state[0] < count:
                state[0] += 1
                return False
            return True

        self.assertEqual(
            utils.retry_bool(wont_recover, times=count-1), False
        )
        self.assertEqual(state[0], count)

    def test_retryable_recover(self):
        state = [0]

        @utils.retryable()
        def will_recover():
            if state[0] == 0:
                state[0] += 1
                raise RuntimeError('Uh oh!')
            return 100

        self.assertEqual(will_recover(), 100)
        self.assertEqual(state[0], 1)

    def test_retryable_recover_times(self):
        retry_times = 5
        state = [0]

        @utils.retryable(times=retry_times)
        def will_recover():
            if state[0] < retry_times:
                state[0] += 1
                raise RuntimeError('Uh oh!')
            return 100

        self.assertEqual(will_recover(), 100)
        self.assertEqual(state[0], retry_times)

    def test_retryable_no_recover(self):
        retry_times = 3
        state = [0]

        @utils.retryable()
        def wont_recover():
            state[0] += 1
            raise RuntimeError('Uh oh!')

        with self.assertRaises(RuntimeError):
            wont_recover()
        self.assertEqual(state[0], retry_times+1)

    def test_select(self):
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
            self.assertEquals(utils.select(dicts, key, value), d)

    def test_ensure_environment(self):
        expectations = (
            (
                [],
                {'A': 'B', 'C': 'D'},
                [],
                None,
            ),
            (
                [],
                {},
                [],
                None
            ),
            (
                ['A'],
                {'A': 'B', 'C': 'D'},
                [],
                None,
            ),
            (
                ['A', 'C'],
                {'A': 'B', 'C': 'D'},
                [],
                None,
            ),
            (
                ['E'],
                {'A': 'B', 'C': 'D'},
                ['E'],
                utils.IncompleteEnvironment,
            ),
            (
                ['A', 'B'],
                {},
                ['A', 'B'],
                utils.IncompleteEnvironment,
            ),
            (
                ['A', 'C'],
                {'A': 'B'},
                ['C'],
                utils.IncompleteEnvironment,
            ),
        )
        for required, env, missing, error in expectations:
            with mock.patch('os.environ', env):
                if not error:
                    out_env = utils.ensure_environment(required)
                    self.assertEqual(out_env, env)
                else:
                    with self.assertRaises(error) as r:
                        utils.ensure_environment(required)
                    variables = ', '.join(missing)
                    message = 'Environment variables not set: {}'.format(
                        variables)
                    self.assertEqual(r.exception.message, message)
                    self.assertEqual(r.exception.variables, missing)
