# -*- encoding: utf-8 -*-
import abc
import re
from abjad.tools.abctools import AbjadObject
from abjad.tools.pitchtools.Accidental import Accidental


class PitchClass(AbjadObject):
    '''Pitch-class base class.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _diatonic_pitch_class_name_regex_body = '''
        ([a-g,A-G]) # exactly one lowercase a - g or uppercase A - G
        '''

    _diatonic_pitch_class_name_regex = re.compile(
        '^{}$'.format(_diatonic_pitch_class_name_regex_body),
        re.VERBOSE,
        )

    _diatonic_pitch_class_name_to_diatonic_pitch_class_number = {
        'c': 0,
        'd': 1,
        'e': 2,
        'f': 3,
        'g': 4,
        'a': 5,
        'b': 6,
        }

    _diatonic_pitch_class_name_to_pitch_class_number = {
        'c': 0,
        'd': 2,
        'e': 4,
        'f': 5,
        'g': 7,
        'a': 9,
        'b': 11,
        }

    _diatonic_pitch_class_number_to_diatonic_pitch_class_name = {
        0: 'c',
        1: 'd',
        2: 'e',
        3: 'f',
        4: 'g',
        5: 'a',
        6: 'b',
        }

    _diatonic_pitch_class_number_to_pitch_class_number = {
        0: 0,
        1: 2,
        2: 4,
        3: 5,
        4: 7,
        5: 9,
        6: 11,
        }

    _pitch_class_name_regex_body = '''
        {}          # exactly one diatonic pitch-class name
        {}          # followed by exactly one alphabetic accidental name
        '''.format(
        _diatonic_pitch_class_name_regex_body,
        Accidental._alphabetic_accidental_regex_body,
        )

    _pitch_class_name_regex = re.compile(
        '^{}$'.format(_pitch_class_name_regex_body),
        re.VERBOSE,
        )

    _pitch_class_number_to_diatonic_pitch_class_number = {
        0: 0,
        2: 1,
        4: 2,
        5: 3,
        7: 4,
        9: 5,
        11: 6,
        }

    _pitch_class_number_to_pitch_class_name = {
        0:    'c',
        0.5:  'cqs',
        1:    'cs',
        1.5:  'dqf',
        2:    'd',
        2.5:  'dqs',
        3:    'ef',
        3.5:  'eqf',
        4:    'e',
        4.5:  'eqs',
        5:    'f',
        5.5:  'fqs',
        6:    'fs',
        6.5:  'gqf',
        7:    'g',
        7.5:  'gqs',
        8:    'af',
        8.5:  'aqf',
        9:    'a',
        9.5:  'aqs',
        10:   'bf',
        10.5: 'bqf',
        11:   'b',
        11.5: 'bqs',
        }

    _pitch_class_number_to_pitch_class_name_with_flats = {
        0:    'c',
        0.5:  'dtqf',
        1:    'df',
        1.5:  'dqf',
        2:    'd',
        2.5:  'etqf',
        3:    'ef',
        3.5:  'eqf',
        4:    'e',
        4.5:  'fqf',
        5:    'f',
        5.5:  'gtqf',
        6:    'gf',
        6.5:  'gqf',
        7:    'g',
        7.5:  'atqf',
        8:    'af',
        8.5:  'aqf',
        9:    'a',
        9.5:  'btqf',
        10:   'bf',
        10.5: 'bqf',
        11:   'b',
        11.5: 'cqf',
        }

    _pitch_class_number_to_pitch_class_name_with_sharps = {
        0:    'c',
        0.5:  'cqs',
        1:    'cs',
        1.5:  'ctqs',
        2:    'd',
        2.5:  'dqs',
        3:    'ds',
        3.5:  'dtqs',
        4:    'e',
        4.5:  'eqs',
        5:    'f',
        5.5:  'fqs',
        6:    'fs',
        6.5:  'ftqs',
        7:    'g',
        7.5:  'gqs',
        8:    'gs',
        8.5:  'gtqs',
        9:    'a',
        9.5:  'aqs',
        10:   'as',
        10.5: 'atqs',
        11:   'b',
        11.5: 'bqs',
        }

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __hash__(self):
        return hash(repr(self))

    ### PRIVATE METHODS ###

    # do not indent in storage
    def _get_tools_package_qualified_repr_pieces(self, is_indented=True):
        from abjad.tools import abctools
        return [''.join(
            abctools.AbjadObject._get_tools_package_qualified_repr_pieces(
                self, is_indented=False))]

    ### PUBLIC METHODS ###

#    @abc.abstractmethod
#    def apply_accidental(self, accidental=None):
#        raise NotImplementedError

#    @abc.abstractmethod
#    def invert(self, axis=None):
#        raise NotImplementedError

    @staticmethod
    def is_diatonic_pitch_class_name(expr):
        '''True when `expr` is a diatonic pitch-class name, otherwise false.

        ::

            >>> pitchtools.PitchClass.is_diatonic_pitch_class_name('c')
            True

        The regex ``^[a-g,A-G]$`` underlies this predicate.

        Return boolean.
        '''
        if not isinstance(expr, str):
            return False
        return bool(PitchClass._diatonic_pitch_class_name_regex.match(expr))

    @staticmethod
    def is_diatonic_pitch_class_number(expr):
        '''True when `expr` is a diatonic pitch-class number, otherwise false.

        ::

            >>> pitchtools.PitchClass.is_diatonic_pitch_class_number(0)
            True

        ::

            >>> pitchtools.PitchClass.is_diatonic_pitch_class_number(-5)
            False

        The diatonic pitch-class numbers are equal to the set
        ``[0, 1, 2, 3, 4, 5, 6]``.

        Return boolean.
        '''
        if expr in range(7):
            return True
        return False

    @staticmethod
    def is_pitch_class_name(expr):
        '''True when `expr` is a chromatic pitch-class name, otherwise false.

        ::

            >>> pitchtools.PitchClass.is_pitch_class_name('fs')
            True

        The regex ``^([a-g,A-G])(([s]{1,2}|[f]{1,2}|t?q?[fs]|)!?)$`` underlies
        this predicate.

        Return boolean.
        '''
        if not isinstance(expr, str):
            return False
        return bool(PitchClass._pitch_class_name_regex.match(expr))

    @staticmethod
    def is_pitch_class_number(expr):
        '''True `expr` is a chromatic pitch-class number, otherwise false.

        ::

            >>> pitchtools.PitchClass.is_pitch_class_number(1)
            True

        The chromatic pitch-class numbers are equal to the set
        ``[0, 0.5, ..., 11, 11.5]``.

        Return boolean.
        '''

        return expr in [(n).__truediv__(2) for n in range(24)]

#    @abc.abstractmethod
#    def multiply(self, n=1):
#        raise NotImplementedError

#    @abc.abstractmethod
#    def transpose(self, expr):
#        raise NotImplementedError

    ### PUBLIC PROPERTIES ###

    @property
    def accidental_spelling(self):
        r'''Accidental spelling.

        ::

            >>> pitchtools.NamedPitch("c").accidental_spelling
            'mixed'

        Return string.
        '''
        from abjad import abjad_configuration
        return abjad_configuration['accidental_spelling']

    @abc.abstractproperty
    def accidental(self):
        r'''Accidental.'''
        raise NotImplementedError

    @abc.abstractproperty
    def alteration_in_semitones(self):
        r'''Alteration in semitones.'''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_class_name(self):
        r'''Diatonic pitch-class name.'''
        raise NotImplementedError

    @abc.abstractproperty
    def diatonic_pitch_class_number(self):
        r'''Diatonic pitch-class number.'''
        raise NotImplementedError

    @abc.abstractproperty
    def named_pitch_class(self):
        r'''Named pitch-class.'''
        raise NotImplementedError

    @abc.abstractproperty
    def numbered_pitch_class(self):
        r'''Numbered pitch-class.'''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_label(self):
        r'''Pitch-class label.'''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_name(self):
        r'''Pitch-class name.'''
        raise NotImplementedError

    @abc.abstractproperty
    def pitch_class_number(self):
        r'''Pitch-class number.'''
        raise NotImplementedError

