# -*- encoding: utf-8 -*-
from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor \
    import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest \
    import TargetManifest
from experimental.tools.scoremanagertools.specifiers.ClefSpecifier \
    import ClefSpecifier


class ClefSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS VARIABLES ###

    target_manifest = TargetManifest(
        ClefSpecifier,
        ('clef_name', 'cf', selectors.Selector.make_clef_name_selector),
        )
