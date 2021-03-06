# -*- encoding: utf-8 -*-
import pytest
from abjad import *
import scoremanager


def test_MaterialPackageManager_screenscrapes_01():
    r'''Score material run from home.
    '''
    pytest.skip('TODO: add Red Example Score time signatures.')


    score_manager = scoremanager.core.ScoreManager()
    score_manager._run(pending_user_input='all red_example_score m black q')

    assert score_manager.io_transcript[-2] == \
    ['Red Example Score (2013) - materials - time signatures',
      '',
      '     material definition - edit (mde)',
      '     material definition - execute (mdx)',
      '',
      '     output material - make (omm)',
      '     output material - view (omv)',
      '',
      '     illustration builder - edit (ibe)',
      '     illustration builder - execute (ibx)',
      '     score stylesheet - select (sss)',
      '',
      '     output pdf - make (pdfm)',
      '     output pdf - view (pdfv)',
      '']


def test_MaterialPackageManager_screenscrapes_02():
    r'''Score material run independently.
    '''
    pytest.skip('TODO: add Red Example Score time signatures.')

    material_manager = scoremanager.managers.MaterialPackageManager(
        'red_example_score.materials.time_signatures')
    material_manager._run(pending_user_input='q')

    assert material_manager.io_transcript[-2] == \
    ['Time signatures',
      '',
      '     material definition - edit (mde)',
      '     material definition - execute (mdx)',
      '',
      '     output material - make (omm)',
      '     output material - view (omv)',
      '',
      '     illustration builder - edit (ibe)',
      '     illustration builder - execute (ibx)',
      '     score stylesheet - select (sss)',
      '',
      '     output pdf - make (pdfm)',
      '     output pdf - view (pdfv)',
      '']
