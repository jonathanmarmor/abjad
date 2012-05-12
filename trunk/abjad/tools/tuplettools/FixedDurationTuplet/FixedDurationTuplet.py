from abjad.tools.tuplettools.Tuplet.Tuplet import Tuplet
from abjad.tools import durationtools
from fractions import Fraction


class FixedDurationTuplet(Tuplet):
    '''Abjad tuplet of fixed duration and variable multiplier:

    ::

        abjad> tuplettools.FixedDurationTuplet(Fraction(2, 8), "c'8 d'8 e'8")
        FixedDurationTuplet(1/4, [c'8, d'8, e'8])

    Return fixed-duration tuplet.
    '''

    __slots__ = ('_target_duration', )

    def __init__(self, duration, music=None, **kwargs):
        # new #
        dummy_multiplier = 1
        Tuplet.__init__(self, dummy_multiplier, music)
        # end #
        self._signifier = '@'
        self.target_duration = duration
        self._initialize_keyword_values(**kwargs)

    ### SPECIAL METHODS ###

    def __getnewargs__(self):
        return (self.target_duration, )

    def __repr__(self):
        return '%s(%s, [%s])' % (type(self).__name__, self.target_duration, self._summary)

    def __str__(self):
        if 0 < len(self):
            return '{%s %s %s %s}' % (self._signifier, self.ratio_string, self._summary, self._signifier)
        else:
            return '{%s %s %s}' % (self._signifier, self.target_duration, self._signifier)

    ### PUBLIC PROPERTIES ###

    @property
    def multiplied_duration(self):
        '''Read-only multiplied duration of tuplet::

            abjad> tuplet = tuplettools.FixedDurationTuplet((1, 4), "c'8 d'8 e'8")
            abjad> tuplet.multiplied_duration
            Duration(1, 4)

        Return duration.
        '''
        return self.target_duration

    @apply
    def multiplier():
        def fget(self):
            '''Read-only multiplier of tuplet::

                abjad> tuplet = tuplettools.FixedDurationTuplet((1, 4), "c'8 d'8 e'8")
                abjad> tuplet.multiplier
                Fraction(2, 3)

            Return fraction.
            '''
            if 0 < len(self):
                return Fraction(self.target_duration / self.contents_duration)
            else:
                return None
        def fset(self, expr):
            pass
        return property(**locals())

    @apply
    def target_duration():
        def fget(self):
            r'''Read / write target duration of fixed-duration tuplet::

                abjad> tuplet = tuplettools.FixedDurationTuplet((1, 4), "c'8 d'8 e'8")
                abjad> tuplet.target_duration
                Duration(1, 4)

            ::

                abjad> f(tuplet)
                \times 2/3 {
                    c'8
                    d'8
                    e'8
                }

            ::

                abjad> tuplet.target_duration = Duration(5, 8)
                abjad> f(tuplet)
                \fraction \times 5/3 {
                    c'8
                    d'8
                    e'8
                }

            Return duration.
            '''
            return self._target_duration
        def fset(self, expr):
            if isinstance(expr, (int, long)):
                rational = durationtools.Duration(expr)
            elif isinstance(expr, tuple):
                rational = durationtools.Duration(*expr)
            elif hasattr(expr, 'numerator') and hasattr(expr, 'denominator'):
                rational = durationtools.Duration(expr)
            else:
                raise ValueError('Can not set tuplet rational from %s.' % str(expr))
            if 0 < rational:
                self._target_duration = rational
            else:
                raise ValueError('Tuplet rational %s must be positive.' % rational)
        return property(**locals())

    ### PUBLIC METHODS ###

    def trim(self, start, stop = 'unused'):
        '''Trim fixed-duration tuplet elements from `start` to `stop`::

            abjad> tuplet = tuplettools.FixedDurationTuplet(Fraction(2, 8), "c'8 d'8 e'8")
            abjad> tuplet
            FixedDurationTuplet(1/4, [c'8, d'8, e'8])

        ::

            abjad> tuplet.trim(2)
            abjad> tuplet
            FixedDurationTuplet(1/6, [c'8, d'8])

        Preserve fixed-duration tuplet multiplier.

        Adjust fixed-duration tuplet duration.

        Return none.
        '''
        if stop != 'unused':
            assert not (start == 0 and (stop is None or len(self) <= stop))
        old_multiplier = self.multiplier
        if stop == 'unused':
            del(self[start])
        else:
            del(self[start:stop])
        self.target_duration = old_multiplier * self.contents_duration
