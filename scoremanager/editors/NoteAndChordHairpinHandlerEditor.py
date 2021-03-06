# -*- encoding: utf-8 -*-
from experimental.tools import handlertools
from scoremanager import getters
from scoremanager.editors.InteractiveEditor import InteractiveEditor


class NoteAndChordHairpinHandlerEditor(InteractiveEditor):

    ### PUBLIC PROPERTIES ###

    @property
    def target_manifest(self):
        return self.TargetManifest(
            handlertools.NoteAndChordHairpinHandler,
            ('hairpin_token', None, 'ht', getters.get_hairpin_token, True),
            ('minimum_duration', None, 'md', getters.get_duration, True),
            )
