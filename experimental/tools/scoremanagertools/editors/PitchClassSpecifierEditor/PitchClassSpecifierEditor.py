from experimental.tools.scoremanagertools import getters
from experimental.tools.scoremanagertools import selectors
from experimental.tools.scoremanagertools import wizards
from experimental.tools.scoremanagertools.editors.ParameterSpecifierEditor import ParameterSpecifierEditor
from experimental.tools.scoremanagertools.editors.TargetManifest import TargetManifest
from experimental.tools.scoremanagertools.specifiers.PitchClassSpecifier import PitchClassSpecifier


class PitchClassSpecifierEditor(ParameterSpecifierEditor):

    ### CLASS ATTRIBUTES ###

    target_manifest = TargetManifest(PitchClassSpecifier,
        ('name', 'nm', getters.get_string),
        ('description', 'ds', getters.get_string),
        (),
        ('pitch_class_reservoir', 'pc', selectors.PitchClassReservoirSelector),
        ('pitch_class_transform', 'tr', wizards.PitchClassTransformCreationWizard),
        ('reservoir_start_helper', 'hp', wizards.ReservoirStartHelperCreationWizard),
        )

    ### READ-ONLY PROPERTIES ###

    @property
    def target_name(self):
        return self.target.name