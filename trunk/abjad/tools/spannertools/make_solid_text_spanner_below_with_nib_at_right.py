# -*- encoding: utf-8 -*-
from abjad.tools import markuptools
from abjad.tools import schemetools


def make_solid_text_spanner_below_with_nib_at_right(left_text, components=None):
    r'''Span `components` with text spanner.
    Position spanner below staff and configure with `left_text`,
    solid line and upward-pointing nib at right:

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8")

    ::

        >>> spannertools.make_solid_text_spanner_below_with_nib_at_right(
        ...     'foo', staff[:])
        TextSpanner(c'8, d'8, e'8, f'8)

    ..  doctest::

        >>> f(staff)
        \new Staff {
            \override TextSpanner #'bound-details #'left #'text = \markup { foo }
            \override TextSpanner #'bound-details #'right #'text = \markup { \draw-line #'(0 . 1) }
            \override TextSpanner #'bound-details #'right-broken #'text = ##f
            \override TextSpanner #'dash-fraction = #1
            \override TextSpanner #'direction = #down
            c'8 \startTextSpan
            d'8
            e'8
            f'8 \stopTextSpan
            \revert TextSpanner #'bound-details #'left #'text
            \revert TextSpanner #'bound-details #'right #'text
            \revert TextSpanner #'bound-details #'right-broken #'text
            \revert TextSpanner #'dash-fraction
            \revert TextSpanner #'direction
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Return spanner.
    '''
    from abjad.tools import spannertools

    text_spanner = spannertools.TextSpanner(components)
    left_text = markuptools.Markup(left_text)
    text_spanner.override.text_spanner.bound_details__left__text = left_text
    right_text = markuptools.Markup(markuptools.MarkupCommand('draw-line', schemetools.SchemePair(0, 1)))
    text_spanner.override.text_spanner.bound_details__right__text = right_text
    text_spanner.override.text_spanner.bound_details__right_broken__text = False
    text_spanner.override.text_spanner.dash_fraction = 1
    text_spanner.override.text_spanner.direction = Down

    return text_spanner
