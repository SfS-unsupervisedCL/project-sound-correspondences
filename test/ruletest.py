# Unit tests for tree/rules.py
import unittest
from tree.rules import *
from preprocessing import features as feat
from sklearn.externals import joblib

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

        rule = (['deu_itself_place', 'deu_prevOrSelfCons_voice',
                 'swe_prevOrSelfNonDot_rounding', 'swe_prevOrSelfCons_manner',
                 'swe_prevOrSelfCons_manner'], [0.5, 1.5, 0.5, 2.0, 6.0],
                [False, False, True, True, True], 'plosive')
        exp = (['deu_itself_place', 'deu_prevOrSelfCons_voice',
                'swe_prevOrSelfNonDot_rounding', 'swe_prevOrSelfCons_manner'],
               [0.5, 1.5, 0.5, 2.0], [False, False, True, True], 'plosive')
        self.assertEqual(exp, shorten_rule(rule))

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


class TestMergeRules(unittest.TestCase):

    def test_too_different(self):
        rule1 = (['a', 'a', 'a'], [4.5, 1.5, 3.5],
                 [True, True, True], 'voiced')
        rule1 = sort(rule1, feature_order)
        rule2 = (['a', 'a', 'a', 'a'], [4.5, 1.5, 3.5, 4.0],
                 [True, True, True, True], 'voiced')
        rule2 = sort(rule2, feature_order)
        self.assertEqual([rule1, rule2], merge_and_shorten_rules(rule1, rule2))

        rule2 = (['a', 'a', 'a'], [4.5, 1.5, 3.5],
                 [True, True, True], 'voiceless')
        rule2 = sort(rule2, feature_order)
        self.assertEqual([rule1, rule2], merge_and_shorten_rules(rule1, rule2))

        rule2 = (['a', 'b', 'a'], [4.5, 1.5, 3.5],
                 [True, True, True], 'voiced')
        rule2 = sort(rule2, feature_order)
        self.assertEqual([rule1, rule2], merge_and_shorten_rules(rule1, rule2))

        rule2 = (['a', 'a', 'a'], [4.0, 1.5, 3.5],
                 [True, True, True], 'voiced')
        rule2 = sort(rule2, feature_order)
        self.assertEqual([rule1, rule2], merge_and_shorten_rules(rule1, rule2))

        rule2 = (['a', 'a', 'a'], [4.5, 1.5, 3.5],
                 [True, False, False], 'voiced')
        rule2 = sort(rule2, feature_order)
        self.assertEqual([rule1, rule2], merge_and_shorten_rules(rule1, rule2))

    def test_identical(self):
        rule = (['a', 'b', 'f', 'z', 'd', 'c'],
                [1, 1, 1, 1, 1, 1],
                [True, True, True, True, True, True],
                'class')
        rule = sort(rule, feature_order)
        self.assertEqual([rule], merge_and_shorten_rules(rule, rule))

    def test_merge(self):
        rule1 = (['a', 'b', 'f', 'z', 'd', 'c'],
                 [1, 1.5, 2.3, 1, 4.6, 1],
                 [True, True, False, False, True, False],
                 'class')
        rule1 = sort(rule1, feature_order)
        rule2 = (['a', 'b', 'f', 'z', 'd', 'c'],
                 [1, 1.5, 2.3, 1, 4.6, 1],
                 [True, True, True, False, True, False],
                 'class')
        rule2 = sort(rule2, feature_order)
        exp = (['a', 'b', 'z', 'd', 'c'],
               [1, 1.5, 1, 4.6, 1],
               [True, True, False, True, False],
               'class')
        exp = sort(exp, feature_order)
        self.assertEqual([exp], merge_and_shorten_rules(rule1, rule2))

        rule2 = (['a', 'b', 'f', 'z', 'd', 'c'],
                 [1, 1.5, 2.3, 1, 4.6, 1],
                 [False, True, False, False, True, False],
                 'class')
        rule2 = sort(rule2, feature_order)
        exp = (['b', 'f', 'z', 'd', 'c'],
               [1.5, 2.3, 1, 4.6, 1],
               [True, False, False, True, False],
               'class')
        exp = sort(exp, feature_order)
        self.assertEqual([exp], merge_and_shorten_rules(rule1, rule2))


def tree():
    clf = joblib.load('test/deu_manner.pkl')
    header = feat.header_list(['deu', 'swe'])
    header.remove('deu_itself_manner')
    header.remove('deu_prevOrSelfNonDot_manner')
    header.remove('deu_prevOrSelfVowel_manner')
    header.remove('deu_prevOrSelfCons_manner')

    classes = ['', 'plosive', 'affricate', 'fricative',
               'lateral approximant', 'approximant', 'nasal']

    features = ['deu_itself_place', 'deu_prevVowel_rounding',
                'deu_prevOrSelfCons_voice', 'swe_itself_manner',
                'swe_prevCons_manner', 'swe_prevOrSelfNonDot_rounding',
                'swe_prevOrSelfCons_manner']
    return clf, header, classes, features


def rule_to_string(features, thresholds, decisions, class_name):
    rule = 'IF '
    for (feature, threshold, decision) in zip(features, thresholds, decisions):
        rule += (feature + ' ' + (u'\u2264' if decision else '>')
                 + ' ' + str(threshold) + ' AND ')
    return rule[:-4] + 'THEN ' + class_name


class TestRuleSetFromTree(unittest.TestCase):

    def test_extraction_and_pruning(self):
        clf, header, classes, features = tree()
        d0t = 'IF ' + features[0] + ' ≤ 0.5 '
        d0f = 'IF ' + features[0] + ' > 0.5 '
        d1t = 'AND ' + features[2] + ' ≤ 1.5 '
        d1f = 'AND ' + features[2] + ' > 1.5 '
        d2t = 'AND ' + features[3] + ' ≤ 4.0 '
        d2f = 'AND ' + features[3] + ' > 4.0 '
        d3t = 'AND ' + features[6] + ' ≤ 6.0 '
        d3f = 'AND ' + features[6] + ' > 6.0 '
        d4t = 'AND ' + features[5] + ' ≤ 0.5 '
        d4f = 'AND ' + features[5] + ' > 0.5 '
        d5t = 'AND ' + features[6] + ' ≤ 2.0 '
        d5f = 'AND ' + features[6] + ' > 2.0 '
        d6t = 'AND ' + features[0] + ' ≤ 3.5 '
        d6f = 'AND ' + features[0] + ' > 3.5 '
        d7t = 'AND ' + features[1] + ' ≤ 0.5 '
        d7f = 'AND ' + features[1] + ' > 0.5 '
        d8t = 'AND ' + features[6] + ' ≤ 7.5 '
        d8f = 'AND ' + features[6] + ' > 7.5 '
        d9t = 'AND ' + features[4] + ' ≤ 6.0 '
        d9f = 'AND ' + features[4] + ' > 6.0 '

        r0 = d0t + 'THEN N/A'
        # r1 includes two merged rules
        r1 = d0f + d1t + d2t + 'THEN plosive'
        r2 = d0f + d1t + d2f + 'THEN fricative'
        # r3 is shortened (d3t is covered by r5t)
        r3 = d0f + d1f + d4t + d5t + 'THEN plosive'
        r4 = d0f + d6t + d1f + d4t + d5f + d3t + 'THEN fricative'
        # r5 and r6 are shortened (d0f is covered by d6f)
        r5 = 'IF' + d6f[3:] + d7t + d1f + d4t + d5f + d3t + 'THEN fricative'
        r6 = 'IF' + d6f[3:] + d7f + d1f + d4t + d5f + d3t + 'THEN plosive'
        r7 = d0f + d1f + d4f + d3t + 'THEN nasal'
        r8 = d0f + d1f + d9t + d3f + d8t + 'THEN lateral approximant'
        r9 = d0f + d1f + d9f + d3f + d8t + 'THEN nasal'
        # r10 includes two merged rules
        # and is shortened (r3f is covered by r8f)
        r10 = d0f + d1f + d8f + 'THEN nasal'

        rules = traverse(clf.tree_, 0, classes, header, [], [], [], [])

        rules = prune_rules(rules, header)

        rules_str = []
        for (features, thresholds, decisions, class_name) in rules:
            rule = rule_to_string(features, thresholds, decisions, class_name)
            rules_str.append(rule)

        self.assertEqual(11, len(rules_str))

        for rule in (r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10):
            self.assertTrue(rule in rules_str)

    def test_all(self):
        clf, header, classes, features = tree()
        d0t = 'IF ' + features[0] + ' is N/A '
        d0f = 'IF ' + features[0] + ' is applicable '
        d1t = 'AND ' + features[2] + ' in {N/A, voiceless} '
        d1f = 'AND ' + features[2] + ' is voiced '
        d2t = 'AND ' + features[3] + ' in {N/A, plosive, tap, trill, affricate} '
        d2f = 'AND ' + features[3] + ' in {fricative, lateral fricative, lateral approximant, approximant, nasal} '
        d3t = 'AND ' + features[6] + ' in {N/A, plosive, tap, trill, affricate, fricative, lateral fricative} '
        d3f = 'AND ' + features[6] + ' in {lateral approximant, approximant, nasal} '
        d4t = 'AND ' + features[5] + ' is N/A '
        d4f = 'AND ' + features[5] + ' is applicable '
        d5t = 'AND ' + features[6] + ' in {N/A, plosive, tap} '
        d5f = 'AND ' + features[6] + ' in {trill, affricate, fricative, lateral fricative, lateral approximant, approximant, nasal} '
        d6t = 'AND ' + features[0] + ' in {N/A, glottal, pharyngeal, uvular} '
        d6f = 'AND ' + features[0] + ' in {velar, palatal, retroflex, alveolo-palatal, postalveolar, alveolar, dental, labiodental, bilabial} '
        d7t = 'AND ' + features[1] + ' is N/A '
        d7f = 'AND ' + features[1] + ' is applicable '
        d8t = 'AND ' + features[6] + ' in {N/A, plosive, tap, trill, affricate, fricative, lateral fricative, lateral approximant} '
        d8f = 'AND ' + features[6] + ' in {approximant, nasal} '
        d9t = 'AND ' + features[4] + ' in {N/A, plosive, tap, trill, affricate, fricative, lateral fricative} '
        d9f = 'AND ' + features[4] + ' in {lateral approximant, approximant, nasal} '

        d0fd6t = 'IF ' + features[0] + ' in {glottal, pharyngeal, uvular} '
        d3td5f = 'AND ' + features[6] + ' in {trill, affricate, fricative, lateral fricative} '
        d3fd8t = 'AND ' + features[6] + ' is lateral approximant '

        r0 = d0t + 'THEN N/A'
        # r1 includes two merged rules
        r1 = d0f + d1t + d2t + 'THEN plosive'
        r2 = d0f + d1t + d2f + 'THEN fricative'
        # r3 is shortened (d3t is covered by r5t)
        r3 = d0f + d1f + d4t + d5t + 'THEN plosive'
        r4 = d0fd6t + d1f + d4t + d3td5f + 'THEN fricative'
        # r5 and r6 are shortened (d0f is covered by d6f)
        r5 = 'IF' + d6f[3:] + d7t + d1f + d4t + d3td5f + 'THEN fricative'
        r6 = 'IF' + d6f[3:] + d7f + d1f + d4t + d3td5f + 'THEN plosive'
        r7 = d0f + d1f + d4f + d3t + 'THEN nasal'
        r8 = d0f + d1f + d9t + d3fd8t + 'THEN lateral approximant'
        r9 = d0f + d1f + d9f + d3fd8t + 'THEN nasal'
        # r10 includes two merged rules
        # and is shortened (r3f is covered by r8f)
        r10 = d0f + d1f + d8f + 'THEN nasal'

        rules = traverse(clf.tree_, 0, classes, header, [], [], [], [])

        rules = prune_rules(rules, header)

        rules_str = []
        for (features, thresholds, decisions, class_name) in rules:
            rule = lists2rule(features, thresholds, decisions, class_name)
            rules_str.append(rule)

        self.assertEqual(11, len(rules_str))

        for rule in (r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10):
            self.assertTrue(rule in rules_str)


if __name__ == '__main__':
    unittest.main()
