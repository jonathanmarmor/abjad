from experimental.tools.scoremanagementtools import specifiers
from experimental import *


def test_ArticulationSpecifierEditor_run_01():

    editor = scoremanagementtools.editors.ArticulationSpecifierEditor()
    editor.run(user_input='artic materials.red_mar done')
    specifier = specifiers.ArticulationSpecifier(articulation_handler_name='materials.red_marcati')

    assert editor.target == specifier