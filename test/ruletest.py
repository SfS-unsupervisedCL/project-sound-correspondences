# Unit tests for tree/rules.py
import unittest
from tree.rules import *

feature_order = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']


def reorder(exp, indices):
    return np.array(exp)[indices].tolist()


class TestSort(unittest.TestCase):

    def test_feature(self):
        exp = (['a', 'b', 'c', 'd', 'f', 'z'],
               [1, 1, 1, 1, 1, 1],
               [True, True, True, True, True, True],
               'class')

        rule = (['a', 'b', 'f', 'z', 'd', 'c'],
                [1, 1, 1, 1, 1, 1],
                [True, True, True, True, True, True],
                'class')
        self.assertEqual(exp, sort(rule, feature_order))

        rule = (['z', 'b', 'a', 'f', 'd', 'c'],
                [1, 1, 1, 1, 1, 1],
                [True, True, True, True, True, True],
                'class')
        self.assertEqual(exp, sort(rule, feature_order))

        self.assertEqual(exp, sort(exp, feature_order))

    def test_decision(self):
        exp = (['a', 'a', 'a', 'a', 'a', 'a'],
               [1, 1, 1, 1, 1, 1],
               [False, False, False, True, True, True],
               'class')

        rule = (['a', 'a', 'a', 'a', 'a', 'a'],
                [1, 1, 1, 1, 1, 1],
                [True, False, False, True, True, False],
                'class')
        self.assertEqual(exp, sort(rule, feature_order))

        rule = (['a', 'a', 'a', 'a', 'a', 'a'],
                [1, 1, 1, 1, 1, 1],
                [True, True, True, False, False, False],
                'class')
        self.assertEqual(exp, sort(rule, feature_order))

        self.assertEqual(exp, sort(exp, feature_order))

    def test_threshold(self):
        exp = (['a', 'a', 'a', 'a', 'a', 'a'],
               [0.5, 0.5, 1.0, 1.5, 2.0, 4.5],
               [True, True, True, True, True, True],
               'class')

        rule = (['a', 'a', 'a', 'a', 'a', 'a'],
                [1.0, 2.0, 0.5, 0.5, 1.5, 4.5],
                [True, True, True, True, True, True],
                'class')
        self.assertEqual(exp, sort(rule, feature_order))

        rule = (['a', 'a', 'a', 'a', 'a', 'a'],
                [4.5, 2.0, 0.5, 0.5, 1.5, 1.0],
                [True, True, True, True, True, True],
                'class')
        self.assertEqual(exp, sort(rule, feature_order))

        self.assertEqual(exp, sort(exp, feature_order))

    def test_combination(self):
        c_exp = ['a', 'a', 'b', 'c', 'c', 'c', 'c', 'd']
        t_exp = [1.5, 1.0, 0.5, 4.5, 1.5, 2.0, 2.5, 4.0]
        d_exp = [False, True, False, False, True, True, True, True]
        exp = (c_exp, t_exp, d_exp, 'class')

        indices = np.array([1, 3, 7, 2, 0, 4, 5, 6])
        rule = (reorder(c_exp, indices),
                reorder(t_exp, indices),
                reorder(d_exp, indices), 'class')
        self.assertEqual(exp, sort(rule, feature_order))

        indices = np.array([7, 6, 5, 4, 3, 2, 1, 0])
        rule = (reorder(c_exp, indices),
                reorder(t_exp, indices),
                reorder(d_exp, indices), 'class')
        self.assertEqual(exp, sort(rule, feature_order))

        self.assertEqual(exp, sort(exp, feature_order))


class TestShortenRule(unittest.TestCase):

    def test_less_than_or_equal(self):
        exp = (['a'], [1.5], [True], 'voiced')

        rule = (['a', 'a'], [4.5, 1.5], [True, True], 'voiced')
        rule = sort(rule, feature_order)
        self.assertEqual(exp, shorten_rule(rule))

        rule = (['a', 'a'], [1.5, 4.5], [True, True], 'voiced')
        rule = sort(rule, feature_order)
        self.assertEqual(exp, shorten_rule(rule))

        rule = (['a', 'a', 'a'], [4.5, 1.5, 3.5],
                [True, True, True], 'voiced')
        rule = sort(rule, feature_order)
        self.assertEqual(exp, shorten_rule(rule))

        rule = (['a', 'a', 'a'], [1.5, 1.5, 1.5],
                [True, True, True], 'voiced')
        rule = sort(rule, feature_order)
        self.assertEqual(exp, shorten_rule(rule))

        self.assertEqual(exp, shorten_rule(exp))

    def test_bigger_than(self):
        exp = (['a'], [4.5], [False], 'voiced')

        rule = (['a', 'a'], [4.5, 1.5], [False, False], 'voiced')
        rule = sort(rule, feature_order)
        self.assertEqual(exp, shorten_rule(rule))

        rule = (['a', 'a'], [1.5, 4.5], [False, False], 'voiced')
        rule = sort(rule, feature_order)
        self.assertEqual(exp, shorten_rule(rule))

        rule = (['a', 'a', 'a'], [4.5, 1.5, 3.5],
                [False, False, False], 'voiced')
        rule = sort(rule, feature_order)
        self.assertEqual(exp, shorten_rule(rule))

        rule = (['a', 'a', 'a'], [4.5, 4.5, 4.5],
                [False, False, False], 'voiced')
        rule = sort(rule, feature_order)
        self.assertEqual(exp, shorten_rule(rule))

    def test_combination_short(self):
        exp = (['a', 'a'], [4.5, 1.5], [False, True], 'voiced')

        rule = (['a', 'a', 'a'],
                [4.5, 1.5, 3.5],
                [False, True, True], 'voiced')
        rule = sort(rule, feature_order)
        self.assertEqual(exp, shorten_rule(rule))

    def test_combination_long(self):
        c_exp = ['a', 'a', 'b', 'c', 'c', 'd']
        t_exp = [1.5, 1.0, 0.5, 4.5, 1.5, 4.0]
        d_exp = [False, True, False, False, True, False]
        exp = (c_exp, t_exp, d_exp, 'class')

        c = ['a', 'a', 'b', 'c', 'c', 'c', 'c', 'd', 'd', 'd']
        t = [1.5, 1.0, 0.5, 4.5, 1.5, 2.0, 2.5, 0.5, 1.0, 4.0]
        d = [False, True, False, False, True, True, True, False, False, False]
        rule = (c, t, d, 'class')
        self.assertEqual(exp, shorten_rule(rule))

    def test_cannot_shorten(self):
        c_exp = ['a', 'a', 'b', 'c', 'c', 'd']
        t_exp = [1.5, 1.0, 0.5, 4.5, 1.5, 4.0]
        d_exp = [False, True, False, False, True, False]
        exp = (c_exp, t_exp, d_exp, 'class')

        self.assertEqual(exp, shorten_rule(exp))

# TODO test merging


if __name__ == '__main__':
    unittest.main()
