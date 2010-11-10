from abjad.tools.componenttools._ignore_parentage_of_components import _ignore_parentage_of_components
from abjad.tools.componenttools._restore_parentage_to_components_by_receipt import _restore_parentage_to_components_by_receipt
from abjad.tools import spannertools
from abjad.tools.marktools._reattach_blinded_marks_to_components_in_expr import \
   _reattach_blinded_marks_to_components_in_expr
import copy


def clone_components_and_covered_spanners(components, n = 1):
   r'''Clone thread-contiguous `components` together with 
   spanners that cover `components`.

   The steps taken in this function are as follows.
   Withdraw `components` from crossing spanners.
   Preserve spanners that `components` cover.
   Deep copy `components`.
   Reapply crossing spanners to source `components`.
   Return copied components with covered spanners. ::

      abjad> voice = Voice(Measure((2, 8), notetools.make_repeated_notes(2)) * 3)
      abjad> macros.diatonicize(voice)
      abjad> beam = spannertools.BeamSpanner(voice.leaves[:4])
      abjad> f(voice)
      \new Voice {
              {
                      \time 2/8
                      c'8 [
                      d'8
              }
              {
                      \time 2/8
                      e'8
                      f'8 ]
              }
              {
                      \time 2/8
                      g'8
                      a'8
              }
      }

   ::

      abjad> result = componenttools.clone_components_and_covered_spanners(voice.leaves)
      abjad> result
      (Note(c', 8), Note(d', 8), Note(e', 8), Note(f', 8), Note(g', 8), Note(a', 8))

   ::

      abjad> new_voice = Voice(result)
      abjad> f(new_voice)
      \new Voice {
              c'8 [
              d'8
              e'8
              f'8 ]
              g'8
              a'8
      }

   ::

      abjad> voice.leaves[0] is new_voice.leaves[0]
      False

   ::

      abjad> voice.leaves[0].beam.spanner is new_voice.leaves[0].beam.spanner
      False

   Clone `components` a total of `n` times. ::

      abjad> result = componenttools.clone_components_and_covered_spanners(voice.leaves[:2], n = 3)
      abjad> result
      (Note(c', 8), Note(d', 8), Note(c', 8), Note(d', 8), Note(c', 8), Note(d', 8))

   ::

      abjad> new_voice = Voice(result)
      abjad> f(new_voice)
      \new Voice {
              c'8
              d'8
              c'8
              d'8
              c'8
              d'8
      }

   .. versionchanged:: 1.1.2
      renamed ``clone.covered( )`` to
      ``componenttools.clone_components_and_covered_spanners( )``.
   '''
   from abjad.tools import componenttools
   
   if n < 1:
      return [ ]

   assert componenttools.all_are_thread_contiguous_components(components)

   spanners = spannertools.get_spanners_that_cross_components(components) 
   for spanner in spanners:
      spanner._block_all_components( )

   receipt = _ignore_parentage_of_components(components)

   result = copy.deepcopy(components)
   for component in result:
      #component._update._mark_all_improper_parents_for_update( )
      component._mark_entire_score_tree_for_later_update('prolated')

   _restore_parentage_to_components_by_receipt(receipt)

   for spanner in spanners:
      spanner._unblock_all_components( )

   for i in range(n - 1):
      result += clone_components_and_covered_spanners(components)

   _reattach_blinded_marks_to_components_in_expr(result)
      
   return result
