from abjad.helpers.assert_components import assert_components
from abjad.helpers.ignore_parent import \
   _ignore_parent
from abjad.tools import spannertools
from abjad.helpers.restore_outgoing_reference_to_parent import \
   restore_outgoing_reference_to_parent
import copy


def unspan(components, n = 1):
   '''Withdraw all components at any level in 'components' from spanners.
      Deep copy unspanned components in 'components'.
      Reapply spanners to all components at any level in 'components'.
      The 'components' must be thread-contiguous.'''

   if n < 1:
      return [ ]

   assert_components(components, contiguity = 'thread')

   spanners = spannertools.get_contained(components) 
   for spanner in spanners:
      spanner._blockAllComponents( )

   receipt = _ignore_parent(components)

   result = copy.deepcopy(components)
   for component in result:
      component._update._markForUpdateToRoot( )

   restore_outgoing_reference_to_parent(receipt)

   for spanner in spanners:
      spanner._unblockAllComponents( )

   for i in range(n - 1):
      result += unspan(components)
      
   return result
