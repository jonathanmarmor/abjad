import os
from experimental import *

score_management_object = scoremanagementtools.core.ScoreManagementObject()


def test_ScoreManagementObject_path_name_to_package_importable_name_01():

    assert score_management_object.path_name_to_package_importable_name(os.environ.get('SCORE_MANAGEMENT_TOOLS_MATERIALS_PATH')) == 'materials'
    assert score_management_object.path_name_to_package_importable_name(os.environ.get('SCORE_MANAGEMENT_TOOLS_SPECIFIERS_PATH')) == 'specifiers'
    assert score_management_object.path_name_to_package_importable_name(os.environ.get('SCORE_MANAGEMENT_TOOLS_CHUNKS_PATH')) == 'sketches'


def test_ScoreManagementObject_path_name_to_package_importable_name_02():

    path = os.path.join(os.environ.get('SCORES'), 'example_score_1')
    assert score_management_object.path_name_to_package_importable_name(path) == 'example_score_1'

    path = os.path.join(os.environ.get('SCORES'), 'example_score_1', 'mus')
    assert score_management_object.path_name_to_package_importable_name(path) == 'example_score_1.mus'

    path = os.path.join(os.environ.get('SCORES'), 'example_score_1', 'mus', 'materials')
    assert score_management_object.path_name_to_package_importable_name(path) == 'example_score_1.mus.materials'


def test_ScoreManagementObject_path_name_to_package_importable_name_03():

    path = os.path.join(os.environ.get('SCORES'), 'example_score_1', 'foo')
    assert score_management_object.path_name_to_package_importable_name(path) == 'example_score_1.foo'

    path = os.path.join(os.environ.get('SCORES'), 'example_score_1', 'foo.py')
    assert score_management_object.path_name_to_package_importable_name(path) == 'example_score_1.foo'