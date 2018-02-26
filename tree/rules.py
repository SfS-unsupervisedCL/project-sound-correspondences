from .tree import build_tree, features_dict
from sklearn.tree import _tree
from copy import deepcopy
import numpy as np
import itertools


def get_rules(clf, class_names, feature_names):
    """
    Extracts the rules from a decision tree classifier.
    The keyword arguments correspond to the objects returned by
    tree.build_tree.

    Keyword arguments:
    clf: A sklearn.tree.DecisionTreeClassifier.
    class_names: A list(str) containing the class names.
    feature_names: A list(str) containing the feature names.

    Returns:
    A list(str) where each element is a rule describing a leaf node.
    """
    tree = clf.tree_
    rules = traverse(tree, 0, class_names, feature_names, [], [], [], [])

    # Sometimes, there are rules with redundant decisions. Replace, e.g.,
    # 'If A > 4 and B <= 6 then class1.' and
    # 'If A > 4 and B > 6 then class1.' with
    # 'If A > 4 then class1.'
    # TODO there should be a more concise way to do this.
    # TODO also what about redundant rules being introduced during this
    # process? is that possible?
    rules_shortened = []
    remove_rules = []
    for (rule1, rule2) in itertools.permutations(rules, 2):
        rules_merged, merged = mergeAndShortenRules(rule1, rule2)
        for r in rules_merged:
            if r not in rules_shortened:
                rules_shortened.append(r)
            if merged:
                if rule1 not in remove_rules:
                    remove_rules.append(rule1)
                if rule2 not in remove_rules:
                    remove_rules.append(rule2)
    for rule in remove_rules:
        rules_shortened.remove(rule)

    rules_str = []
    for (features, thresholds, decisions, class_name) in rules_shortened:
        rule = lists2rule(features, thresholds, decisions, class_name)
        rules_str.append(rule)
    return rules_str


def traverse(tree, node,
             class_names, feature_names,
             features, thresholds, decisions, rules):
    """
    A recusive method for performing a pre-order traversal of a given tree,
    while collecting the rules it contains.

    Keyword arguments:
    tree: A sklearn.tree._tree.Tree.
    node: An integer corresponding to the index of the current tree node.
    class_names: A list(str) containing the class names.
    feature_names: A list(str) containing the feature names.
    features: A list(str) containing the decision node features
              on the path to the current node.
    thresholds: A list(float) containing the decision node thresholds
                on the path to the current node, corresponding to `features`.
    decisions: A list(bool) containing the decisions on the path to the current
               node, corresponding to `features` and `thresholds`.
    rules: A list(tuple(list(str), list(float), list(bool), str))
           containing the rules encountered so far.

    Returns:
    rules: A list(tuple(list(str), list(float), list(bool), str))
           containing the rules encountered so far.
    """

    # Note: sklearn.tree._tree.Tree is a collection of parallel arrays where
    # the indices correspond to the nodes, as encountered in a pre-order
    # traversal.

    if tree.feature[node] == _tree.TREE_UNDEFINED:
        # leaf node
        # tree.value contains the class distributions
        class_name = int2class(tree.value[node], class_names)
        rule = (deepcopy(features), deepcopy(thresholds), deepcopy(decisions),
                deepcopy(class_name))
        rules.append(rule)
        features.pop()
        thresholds.pop()
        decisions.pop()
        return rules

    feature = feature_names[tree.feature[node]]
    features.append(feature)
    threshold = tree.threshold[node]
    thresholds.append(threshold)

    # The left child corresponds to True, the right one to False.
    decisions.append(True)
    traverse(tree, tree.children_left[node],
             class_names, feature_names,
             deepcopy(features), deepcopy(thresholds), deepcopy(decisions),
             rules)

    decisions[len(decisions) - 1] = False
    traverse(tree, tree.children_right[node],
             class_names, feature_names,
             features, thresholds, decisions, rules)

    return rules


def int2class(value, class_names):
    class_name = class_names[np.argmax(value)]
    if class_name == '':
        class_name = 'N/A'
    return class_name


def lists2rule(features, thresholds, decisions, class_name):
    """
    Transforms the given lists into a string containing the rule that
    describes a lef node.
    Assumes that len(features) == len(thresholds) == len(decisions).

    Keyword arguments:
    features: A list(str) containing the decision node features
              on the path to the leaf node.
    thresholds: A list(float) containing the decision node thresholds
                on the path to the leaf node, corresponding to `features`.
    decisions: A list(bool) containing the decisions on the path to the leaf
               node, corresponding to `features` and `thresholds`.
    class_name: A str describing the class predicted by the leaf node.

    Returns:
    rule: The rule.
    """
    rule = 'IF '
    for (feature, threshold, decision) in zip(features, thresholds, decisions):
        rule += (feature + ' ' + ('<=' if decision else '>')
                 + ' ' + str(threshold) + ' AND ')
    return rule[:-4] + 'THEN ' + class_name


def mergeAndShortenRules(rule1, rule2):
    """
    If possible, this method merges the given rules.


    >>> mergeAndShortenRules((['deu_itself_place', 'swe_itself_voice'],
                              [0.5, 1.5], [False, True], 'voiced'),
                              (['deu_itself_place', 'swe_itself_voice'],
                              [0.5, 1.5], [False, False], 'voiced'))
    (['deu_itself_place'], [0.5], [False], 'voiced')

    Keyword arguments:
    rule1: A tuple(list(str), list(float), list(bool), str).
    rule2: A tuple(list(str), list(float), list(bool), str).

    Returns:
    A list(tuple(list(str), list(float), list(bool), str))
    of length 1 (if the lists could be merged) or else 2.
    """
    (features1, thresholds1, decisions1, class_name1) = rule1
    (features2, thresholds2, decisions2, class_name2) = rule2
    # Two rules can be merged + shortened
    # if they are identical except for one decision.
    if (class_name1 != class_name2 or
            len(decisions1) != len(decisions2) or
            features1 != features2 or
            thresholds1 != thresholds2):  # TODO /!\ floats!
        # too many differences
        return [rule1, rule2], False

    diff_index = -1
    for index, (dec1, dec2) in enumerate(zip(decisions1, decisions2)):
        if dec1 != dec2:
            if diff_index != -1:
                # more than one different decision
                return [rule1, rule2], False
            diff_index = index

    if diff_index == -1:
        # identical rules
        return [rule1], True

    return [(features1[:diff_index] + features1[diff_index + 1:],
             thresholds1[:diff_index] + thresholds1[diff_index + 1:],
             decisions1[:diff_index] + decisions1[diff_index + 1:],
             class_name1)], True


if __name__ == "__main__":
    clf, header, class_names = build_tree('data\deu-swe-features.csv',
                                          'output',
                                          'deu_itself_voice',
                                          features_dict['voice'])
    rules = get_rules(clf, class_names, header)
    print()
    for rule in rules:
        print(rule)
