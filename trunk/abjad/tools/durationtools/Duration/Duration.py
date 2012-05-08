from abjad.tools.abctools import ImmutableAbjadObject
from fractions import Fraction


# TODO: allow Duration('8..') initialization
class Duration(ImmutableAbjadObject, Fraction):
    '''.. versionadded:: 2.0

    Abjad model of musical duration.

    Initialize from integer numerator and denominator::

        abjad> Duration(15, 16)
        Duration(15, 16)

    Initialize from integer numerator alone::

        abjad> Duration(2)
        Duration(2, 1)

    Initialize from integer-equivalent numerator and denominator::

        abjad> Duration('15', 16.0)
        Duration(15, 16)

    Durations inherit from built-in fraction.

    Durations are immutable.
    '''

    def __new__(klass, *args):
        from abjad.tools import sequencetools
        if len(args) == 1 and sequencetools.is_integer_equivalent_singleton(args[0]):
            self = Fraction.__new__(klass, int(args[0]))
        elif len(args) == 1 and sequencetools.is_fraction_equivalent_pair(args[0]):
            self = Fraction.__new__(klass, int(args[0][0]), int(args[0][1]))
        elif sequencetools.all_are_integer_equivalent_exprs(args):
            self = Fraction.__new__(klass, *[int(x) for x in args])
        else:
            self = Fraction.__new__(klass, *args)
        return self

    ### SPECIAL METHODS ###

    def __abs__(self, *args):
        return type(self)(Fraction.__abs__(self, *args))

    def __add__(self, *args):
        return type(self)(Fraction.__add__(self, *args))

    def __div__(self, *args):
        return type(self)(Fraction.__div__(self, *args))

    def __divmod__(self, *args):
        return type(self)(Fraction.__divmod__(self, *args))

    def __eq__(self, arg):
        return Fraction.__eq__(self, arg)

    def __ge__(self, arg):
        return Fraction.__ge__(self, arg)

    def __gt__(self, arg):
        return Fraction.__gt__(self, arg)        

    def __le__(self, arg):
        return Fraction.__le__(self, arg)

    def __lt__(self, arg):
        return Fraction.__lt__(self, arg)

    def __mod__(self, *args):
        return type(self)(Fraction.__mod__(self, *args))

    def __mul__(self, *args):
        return type(self)(Fraction.__mul__(self, *args))

    def __neg__(self, *args):
        return type(self)(Fraction.__neg__(self, *args))

    def __ne__(self, arg):
        return Fraction.__ne__(self, arg)

    def __pos__(self, *args):
        return type(self)(Fraction.__pos__(self, *args))

    def __pow__(self, *args):
        return type(self)(Fraction.__pow__(self, *args))

    def __radd__(self, *args):
        return type(self)(Fraction.__radd__(self, *args))

    def __rdiv__(self, *args):
        return type(self)(Fraction.__rdiv__(self, *args))

    def __rdivmod__(self, *args):
        return type(self)(Fraction.__rdivmod__(self, *args))

    def __repr__(self):
        return '%s(%s, %s)' % (type(self).__name__, self.numerator, self.denominator)

    def __rmod__(self, *args):
        return type(self)(Fraction.__rmod__(self, *args))

    def __rmul__(self, *args):
        return type(self)(Fraction.__rmul__(self, *args))

    def __rpow__(self, *args):
        return type(self)(Fraction.__rpow__(self, *args))

    def __rsub__(self, *args):
        return type(self)(Fraction.__rsub__(self, *args))

    def __rtruediv__(self, *args):
        return type(self)(Fraction.__rtruediv__(self, *args))

    def __sub__(self, *args):
        return type(self)(Fraction.__sub__(self, *args))

    def __truediv__(self, *args):
        return type(self)(Fraction.__truediv__(self, *args))

    ### PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _mandatory_argument_values(self):
        result = []
        result.append(self.numerator)
        result.append(self.denominator)
        return tuple(result)
