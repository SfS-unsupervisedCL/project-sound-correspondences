from .tree import build_tree, features_dict
from sklearn.tree import _tree
from copy import deepcopy
import numpy as np


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
    return traverse(tree, 0, class_names, feature_names, [], [], [], [])


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
    rules: A list(str) containing the rules encountered so far.

    Returns:
    rules: A list(str) containing the rules encountered so far.
    """

    # Note: sklearn.tree._tree.Tree is a collection of parallel arrays where
    # the indices correspond to the nodes, as encountered in a pre-order
    # traversal.

    if tree.feature[node] == _tree.TREE_UNDEFINED:
        # leaf node
        # tree.value contains the class distributions
        class_name = int2class(tree.value[node], class_names)
        rule = lists2rule(features, thresholds, decisions, class_name)
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


if __name__ == "__main__":
    clf, header, class_names = build_tree('data\deu-swe-features.csv',
                                          'output',
                                          'deu_itself_voice',
                                          features_dict['voice'])
    rules = get_rules(clf, class_names, header)
    for rule in rules:
        print(rule)
