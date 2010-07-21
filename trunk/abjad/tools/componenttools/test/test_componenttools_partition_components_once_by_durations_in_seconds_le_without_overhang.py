from abjad import *


def test_componenttools_partition_components_once_by_durations_in_seconds_le_without_overhang_01( ):
   '''Fill parts less than durations.'''

   t = Staff(RigidMeasure((2, 8), leaftools.make_repeated_notes(2)) * 4)
   pitchtools.diatonicize(t)
   tempo_spanner = TempoSpanner(t[:])
   tempo_indication = tempotools.TempoIndication(Rational(1, 4), 60)
   tempo_spanner.tempo_indication = tempo_indication

   r'''
   \new Staff {
         \time 2/8
         \tempo 4=60
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
         %% tempo 4=60 ends here
   }
   '''

   groups = \
      componenttools.partition_components_once_by_durations_in_seconds_le_without_overhang(
         t.leaves, [0.75])

   "[[Note(c', 8)]]"

   assert len(groups) == 1
   assert groups[0] == list(t.leaves[:1])
