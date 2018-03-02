from preprocessing import transform_ipa as tipa
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
    rules = prune_rules(rules, feature_names)

    rules_str = []
    for (features, thresholds, decisions, class_name) in rules:
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
        try:
            features.pop()
            thresholds.pop()
            decisions.pop()
        except IndexError:
            # The entire tree is a single leaf node.
            pass
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

    decisions[-1] = False
    traverse(tree, tree.children_right[node],
             class_names, feature_names,
             features, thresholds, decisions, rules)

    return rules


def int2class(value, class_names):
    """Returns the string version of an integer class code."""
    class_name = class_names[np.argmax(value)]
    if class_name == '':
        class_name = 'N/A'
    return class_name


def prune_rules(rules, feature_names):
    """Removes redundancies from the given rules."""

    if len(rules) == 1:
        return rules

    rules = [sort(rule, feature_names) for rule in rules]

    # Sometimes, there are pairs of rules with redundant decisions.
    # Replace, e.g.,
    # 'If A > 4 and B <= 6 then class1.' and
    # 'If A > 4 and B > 6 then class1.' with
    # 'If A > 4 then class1.'
    rules_pruned = rules
    remove_rules = []
    change_rules = True

    while change_rules:
        remove_rules = []

        rules = deepcopy(rules_pruned)
        rules_pruned = []
        for (rule1, rule2) in itertools.combinations(rules, 2):
            rules_merged = merge_and_shorten_rules(rule1, rule2)
            for r in rules_merged:
                if r not in rules_pruned:
                    rules_pruned.append(r)
            if len(rules_merged) == 1:
                remove_rules += [rule1, rule2]

        for rule in remove_rules:
            try:
                rules_pruned.remove(rule)
            except ValueError:
                pass

        change_rules = len(remove_rules) > 0

    # Sometimes, a rule contains redundant decisions.
    # Replace, e.g.,
    # 'If A > 4 and A > 6 then class1.' with
    # 'If A > 6 then class1.'
    rules_pruned = [shorten_rule(rule) for rule in rules_pruned]

    return rules_pruned


def sort(rule, feature_order):
    """
    Sorts the parallel lists that a rule consists of such that the rules can
    be pruned by shorten_rule and merge_and_shorten_rules.

    Keyword arguments:
    rule: A tuple(list(str), list(float), list(bool), str).
    feature_order: A list(str) containing the names of at least the features
                   that are part of the rule.

    Returns:
    A tuple(list(str), list(float), list(bool), str)--the sorted rule.
    """
    (features, thresholds, decisions, class_name) = rule
    # primary sort order: features
    indices = [feature_order.index(x) for x in features]
    # secondary sort order: decisions
    indices = [x + 0.1 if decisions[i] else x for i, x in enumerate(indices)]
    # tertiary sort order: thresholds
    indices = [x + (thresholds[i] / 1000.) for i, x in enumerate(indices)]
    indices = np.array(indices).argsort()
    features = np.array(features)[indices]
    thresholds = np.array(thresholds)[indices]
    decisions = np.array(decisions)[indices]
    return (features.tolist(), thresholds.tolist(), decisions.tolist(),
            class_name)


def shorten_rule(rule):
    """
    If possible, this method removes redundant parts of the given rule.

    >>> shorten_rule((['ukr_itself_place', 'ukr_itself_place'],
                     [4.5, 1.5], [True, True], 'voiced'))
    (['ukr_itself_place'], [1.5], [True], 'voiced')

    Keyword arguments:
    rule: A tuple(list(str), list(float), list(bool), str)
          that represents a sorted rule.

    Returns:
    A tuple(list(str), list(float), list(bool), str) that is either identical
    to `rule` or a pruned version of it.
    """
    if len(rule) < 2:
        return rule

    remove_indices = []
    (features, thresholds, decisions, class_name) = rule

    for i in range(1, len(features)):
        if features[i] != features[i - 1]:
            continue
        if decisions[i] and decisions[i - 1]:  # less-than-or-equal-to
            remove_indices.append(i)
        elif (not decisions[i]) and (not decisions[i - 1]):  # bigger than
            remove_indices.append(i - 1)

    lists = [features, thresholds, decisions]
    for idx in range(len(lists)):
        lists[idx] = [x for i, x in enumerate(lists[idx])
                      if i not in remove_indices]

    return (*lists, class_name)


def merge_and_shorten_rules(rule1, rule2):
    """
    If possible, this method merges the given rules.

    >>> merge_and_shorten_rules((['deu_itself_place', 'swe_itself_voice'],
                                 [0.5, 1.5], [False, True], 'voiced'),
                                (['deu_itself_place', 'swe_itself_voice'],
                                 [0.5, 1.5], [False, False], 'voiced'))
    (['deu_itself_place'], [0.5], [False], 'voiced')

    Keyword arguments:
    rule1: A tuple(list(str), list(float), list(bool), str)
           that represents a sorted rule.
    rule2: A tuple(list(str), list(float), list(bool), str)
           that represents a sorted rule.

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
        return [rule1, rule2]

    diff_index = -1
    for index, (dec1, dec2) in enumerate(zip(decisions1, decisions2)):
        if dec1 != dec2:
            if diff_index != -1:
                # more than one different decision
                return [rule1, rule2]
            diff_index = index

    if diff_index == -1:
        # identical rules
        return [rule1]

    return [(features1[:diff_index] + features1[diff_index + 1:],
             thresholds1[:diff_index] + thresholds1[diff_index + 1:],
             decisions1[:diff_index] + decisions1[diff_index + 1:],
             class_name1)]


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
    A str representing the rule.
    """
    rule = 'IF '

    i = 0
    while i < len(features):
        feature, threshold, decision = features[i], thresholds[i], decisions[i]
        try:
            if feature == features[i + 1]:
                # If a segment like 'A > 2'
                # is followed by a segment like 'A < 7',
                # merge them (e.g. '2 <= A < 7').
                rule += (rule_segment2string(features[i + 1],
                                             thresholds[i + 1],
                                             decisions[i + 1],
                                             lower_bound=threshold) + ' AND ')
                i += 2
                continue
        except IndexError:
            pass
        rule += rule_segment2string(feature, threshold, decision) + ' AND '
        i += 1

    return rule[:-4] + 'THEN ' + class_name


def rule_segment2string(feature, threshold, decision, lower_bound=-1):
    if threshold == 0.5 and not decision:
        return feature + ' is applicable'

    feature_name = feature.split('_')[-1]
    if feature_name == 'type':
        feature_name = 'sound_type'
    feature_str = getattr(tipa, feature_name)
    feature_str[0] = 'N/A'

    threshold = int(threshold) + 1
    lower_bound = int(lower_bound) + 1
    feature_str = (feature_str[lower_bound:threshold] if decision
                   else feature_str[threshold:])

    if len(feature_str) == 1:
        return feature + ' is ' + feature_str[0]
    return feature + ' in {' + ', '.join(feature_str) + '}'
