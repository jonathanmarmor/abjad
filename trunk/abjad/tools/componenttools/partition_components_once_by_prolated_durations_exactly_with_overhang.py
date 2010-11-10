from abjad.tools.componenttools._partition_components_by_durations import _partition_components_by_durations


def partition_components_once_by_prolated_durations_exactly_with_overhang(components, prolated_durations):
   '''Partition `components` once by exact `prolated_durations` and
   allow for overhang components at end.
   '''
   
   parts = _partition_components_by_durations('prolated', components, prolated_durations, 
      fill = 'exact', cyclic = False, overhang = True)

   return parts
