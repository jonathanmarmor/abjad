# -*- encoding: utf-8 -*-
from abjad.tools.stringtools.strip_diacritics_from_binary_string import strip_diacritics_from_binary_string


def string_to_accent_free_underscored_delimited_lowercase(string):
    '''.. versionadded:: 2.6

    Change `string` to strict directory name::

        >>> stringtools.string_to_accent_free_underscored_delimited_lowercase('Déja vu')
        'deja_vu'

    Strip accents from accented characters.
    Change all punctuation (including spaces) to underscore.
    Set to lowercase.

    Return string.
    '''

    assert isinstance(string, str)

    result = strip_diacritics_from_binary_string(string)
    result = result.replace(' ', '_')
    result = result.replace("'", '_')
    result = result.lower()

    return result