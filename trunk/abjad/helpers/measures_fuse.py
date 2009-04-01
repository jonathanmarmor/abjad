from abjad.helpers.assess_components import assess_components
from abjad.helpers.components_switch_parent_to import \
   _components_switch_parent_to
from abjad.helpers.container_scale import container_scale
from abjad.helpers.get_parent_and_indices import get_parent_and_indices
from abjad.helpers.give_dominant_spanners_to import _give_dominant_spanners_to
from abjad.helpers.is_measure_list import _is_measure_list
from abjad.helpers.make_best_meter import _make_best_meter
from abjad.measure.rigid.measure import RigidMeasure
from abjad.meter.meter import Meter


def measures_fuse(measure_list):
   '''Fuse measures in measure_list.
      Calculate best new time signature.'''

   assert _is_measure_list(measure_list)

   if len(measure_list) == 0:
      return None

   if len(measure_list) == 1:
      return measure_list[0]

   parent, parent_index, stop_index = get_parent_and_indices(measure_list)

   old_denominators = [x.meter.effective.denominator for x in measure_list]
   new_duration = sum([x.meter.effective.duration for x in measure_list])

   new_meter = _make_best_meter(new_duration, old_denominators)

   music = [ ]
   for measure in measure_list:
      multiplier = ~new_meter.multiplier * measure.meter.effective.multiplier
      measure_music = measure[:]
      container_scale(measure_music, multiplier)
      music += measure_music

   _components_switch_parent_to(music, None)
   new_measure = RigidMeasure(new_meter, music)
   _components_switch_parent_to(measure_list, None)
   parent.insert(parent_index, new_measure)

   for measure in measure_list:
      _give_dominant_spanners_to([measure], [new_measure])

   return new_measure 
