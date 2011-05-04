from abjad.components import Rest
from abjad.tools import componenttools


def iterate_rests_forward_in_expr(expr, start = 0, stop = None):
   r'''.. versionadded:: 1.1.2

   Iterate rests forward in `expr`::

      abjad> staff = Staff("<e' g' c''>8 a'8 r8 <d' f' b'>8 r2")

   ::

      abjad> f(staff)
      \new Staff {
         <e' g' c''>8
         a'8
         r8
         <d' f' b'>8
         r2
      }

   ::

      abjad> for rest in resttools.iterate_rests_forward_in_expr(staff):
      ...   rest
      Rest('r8')
      Rest('r2')

   Ignore threads.

   Return generator.
   '''
   
   return componenttools.iterate_components_forward_in_expr(
      expr, Rest, start = start, stop = stop)
