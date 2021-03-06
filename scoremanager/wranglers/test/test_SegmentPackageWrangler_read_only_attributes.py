# -*- encoding: utf-8 -*-
from abjad import *
import scoremanager


def test_SegmentPackageWrangler_read_only_attributes_01():

    score_manager = scoremanager.core.ScoreManager()
    wrangler = score_manager.segment_package_wrangler
    assert not wrangler.session.is_in_score

    assert wrangler._breadcrumb == 'segments'
    assert wrangler._current_storehouse_packagesystem_path is None

    parts = ('segments',)
    assert wrangler.score_package_asset_storehouse_path_infix_parts == parts

    assert wrangler._temporary_asset_package_path == '__temporary_package'


def test_SegmentPackageWrangler_read_only_attributes_02():

    score_manager = scoremanager.core.ScoreManager()
    wrangler = score_manager.segment_package_wrangler
    wrangler.session.snake_case_current_score_name = 'red_example_score'
    assert wrangler.session.is_in_score

    assert wrangler._breadcrumb == 'segments'

    string = 'scoremanager.scorepackages.red_example_score.segments'
    assert wrangler._current_storehouse_packagesystem_path == string

    parts = ('segments',)
    assert wrangler.score_package_asset_storehouse_path_infix_parts == parts

    string = 'scoremanager.scorepackages.red_example_score.segments'
    string += '.__temporary_package'
    assert wrangler._temporary_asset_package_path == string
