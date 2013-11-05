# -*- encoding: utf-8 -*-
# TODO: make public and move to bound method of some class
def _grob_attribute_and_value_to_lilypond_override(grob, attribute, value):
    from abjad.tools import formattools

    attribute = formattools.LilyPondFormatManager.format_lilypond_attribute(attribute)
    value = formattools.LilyPondFormatManager.format_lilypond_value(value)
    return r'\once \override {} {} = {}'.format(grob, attribute, value)