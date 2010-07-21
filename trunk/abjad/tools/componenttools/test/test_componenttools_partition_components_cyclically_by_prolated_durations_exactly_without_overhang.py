from abjad import *


def test_componenttools_partition_components_cyclically_by_prolated_durations_exactly_without_overhang_01( ):

   t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 4)
   pitchtools.diatonicize(t)

   r'''
   \new Staff {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8
         f'8
         \time 2/8
         g'8
         a'8
         \time 2/8
         b'8
         c''8
   }
   '''

   groups = \
      componenttools.partition_components_cyclically_by_prolated_durations_exactly_without_overhang(
      t.leaves, [Rational(3, 8)])

   "[[Note(c'', 8), Note(b', 8), Note(a', 8)], [Note(g', 8), Note(f', 8), Note(e', 8)]]"

   assert len(groups) == 2
   assert groups[0] == list(t.leaves[:3])
   assert groups[1] == list(t.leaves[3:6])
