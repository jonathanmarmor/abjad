import copy


def copy_components_and_covered_spanners(components, n=1):
    r'''.. versionadded:: 1.1

    Copy `components` and covered spanners.

    The `components` must be thread-contiguous.

    Covered spanners are those spanners that cover `components`.

    The steps taken in this function are as follows.
    Withdraw `components` from crossing spanners.
    Preserve spanners that `components` cover.
    Deep copy `components`.
    Reapply crossing spanners to source `components`.
    Return copied components with covered spanners. ::

        >>> voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
        >>> pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(voice)
        >>> beam = beamtools.BeamSpanner(voice.leaves[:4])
        >>> f(voice)
        \new Voice {
            {
                \time 2/8
                c'8 [
                d'8
            }
            {
                e'8
                f'8 ]
            }
            {
                g'8
                a'8
            }
        }

    ::

        >>> result = componenttools.copy_components_and_covered_spanners(voice.leaves)
        >>> result
        (Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8"), Note("g'8"), Note("a'8"))

    ::

        >>> new_voice = Voice(result)
        >>> f(new_voice)
        \new Voice {
            c'8 [
            d'8
            e'8
            f'8 ]
            g'8
            a'8
        }

    ::

        >>> voice.leaves[0] is new_voice.leaves[0]
        False

    Copy `components` a total of `n` times. ::

        >>> result = componenttools.copy_components_and_covered_spanners(voice.leaves[:2], n=3)
        >>> result
        (Note("c'8"), Note("d'8"), Note("c'8"), Note("d'8"), Note("c'8"), Note("d'8"))

    ::

        >>> new_voice = Voice(result)
        >>> f(new_voice)
        \new Voice {
            c'8
            d'8
            c'8
            d'8
            c'8
            d'8
        }

    .. versionchanged:: 2.0
        renamed ``clone.covered()`` to
        ``componenttools.copy_components_and_covered_spanners()``.

    .. versionchanged:: 2.0
        renamed ``componenttools.clone_components_and_covered_spanners()`` to
        ``componenttools.copy_components_and_covered_spanners()``.
    '''
    from abjad.tools import componenttools
    from abjad.tools import iterationtools
    from abjad.tools import spannertools
    from abjad.tools.componenttools._ignore_parentage_of_components import _ignore_parentage_of_components
    from abjad.tools.componenttools._restore_parentage_to_components_by_receipt import \
        _restore_parentage_to_components_by_receipt
    from abjad.tools.marktools._reattach_blinded_marks_to_components_in_expr import \
        _reattach_blinded_marks_to_components_in_expr

    if n < 1:
        return []

    assert componenttools.all_are_thread_contiguous_components(components)

    # copy components without spanners
    new_components = [
        component._copy_with_children_and_marks_but_without_spanners() for component in components]
    new_components = type(components)(new_components)

    # make schema of spanners covered by components
    schema = spannertools.make_covered_spanner_schema(components)

    # copy spanners covered by components
    for covered_spanner, component_indices in schema.items():
        new_covered_spanner = copy.deepcopy(covered_spanner)
        del(schema[covered_spanner])
        schema[new_covered_spanner] = component_indices

    # reverse schema
    reversed_schema = {}
    for new_covered_spanner, component_indices in schema.items():
        for component_index in component_indices:
            try:
                reversed_schema[component_index].append(new_covered_spanner)
            except KeyError:
                reversed_schema[component_index] = [new_covered_spanner]

    # iterate components and add new components to new spanners
    for component_index, new_component in enumerate(
        iterationtools.iterate_components_in_expr(new_components)):
        try:
            new_covered_spanners = reversed_schema[component_index]
            for new_covered_spanner in new_covered_spanners:
                new_covered_spanner.append(new_component)
        except KeyError:
            pass

    # repeat as specified by input
    for i in range(n - 1):
        new_components += copy_components_and_covered_spanners(components)

    # return new components
    return new_components
