# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.timeintervaltools import *
from abjad.tools.timeintervaltools.TimeInterval import TimeInterval


def test_timeintervaltools_TimeIntervalTree_find_intervals_starting_and_stopping_within_interval_01():
    blocks = timeintervaltools.make_test_intervals()
    target_interval = TimeInterval(-10, 0)
    expected_payloads = ()
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_starting_and_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_timeintervaltools_TimeIntervalTree_find_intervals_starting_and_stopping_within_interval_02():
    blocks = timeintervaltools.make_test_intervals()
    target_interval = TimeInterval(0, 9)
    expected_payloads = ('a', 'd',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_starting_and_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_timeintervaltools_TimeIntervalTree_find_intervals_starting_and_stopping_within_interval_03():
    blocks = timeintervaltools.make_test_intervals()
    target_interval = TimeInterval(4, 19)
    expected_payloads = ('b', 'c', 'd', 'g',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_starting_and_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_timeintervaltools_TimeIntervalTree_find_intervals_starting_and_stopping_within_interval_04():
    blocks = timeintervaltools.make_test_intervals()
    target_interval = TimeInterval(6, 10)
    expected_payloads = ('c', 'd',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_starting_and_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_timeintervaltools_TimeIntervalTree_find_intervals_starting_and_stopping_within_interval_05():
    blocks = timeintervaltools.make_test_intervals()
    target_interval = TimeInterval(13, 15)
    expected_payloads = ()
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_starting_and_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_timeintervaltools_TimeIntervalTree_find_intervals_starting_and_stopping_within_interval_06():
    blocks = timeintervaltools.make_test_intervals()
    target_interval = TimeInterval(14, 25)
    expected_payloads = ('e', 'f', 'g', 'h',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_starting_and_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_timeintervaltools_TimeIntervalTree_find_intervals_starting_and_stopping_within_interval_07():
    blocks = timeintervaltools.make_test_intervals()
    target_interval = TimeInterval(19, 26)
    expected_payloads = ('h',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_starting_and_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_timeintervaltools_TimeIntervalTree_find_intervals_starting_and_stopping_within_interval_08():
    blocks = timeintervaltools.make_test_intervals()
    target_interval = TimeInterval(24, 31)
    expected_payloads = ('i', 'j',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_starting_and_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_timeintervaltools_TimeIntervalTree_find_intervals_starting_and_stopping_within_interval_09():
    blocks = timeintervaltools.make_test_intervals()
    target_interval = TimeInterval(26, 29)
    expected_payloads = ('j',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_starting_and_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks

def test_timeintervaltools_TimeIntervalTree_find_intervals_starting_and_stopping_within_interval_10():
    blocks = timeintervaltools.make_test_intervals()
    target_interval = TimeInterval(30, 40)
    expected_payloads = ('k', 'l',)
    expected_blocks = TimeIntervalTree([x for x in blocks if x['name'] in expected_payloads])
    for i in range(len(blocks)):
        blocks.append(blocks.pop(0)) # rotate to permute tree construction
        tree = TimeIntervalTree(blocks)
        actual_blocks = tree.find_intervals_starting_and_stopping_within_interval(target_interval)
        assert expected_blocks == actual_blocks