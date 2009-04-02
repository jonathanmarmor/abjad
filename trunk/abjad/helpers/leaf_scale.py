from abjad.exceptions.exceptions import AssignabilityError
from abjad.helpers.bequeath import bequeath
from abjad.helpers.converge_to_power2 import _converge_to_power2
from abjad.helpers.copy_unspan import copy_unspan
from abjad.helpers.duration_token_decompose import _duration_token_decompose
from abjad.helpers.duration_token_unpack import _duration_token_unpack
from abjad.helpers.iterate import iterate
from abjad.helpers.withdraw_from_attached_spanners import \
   _withdraw_from_attached_spanners
from abjad.leaf.leaf import _Leaf
from abjad.rational.rational import Rational
from abjad.tuplet.fd.tuplet import FixedDurationTuplet


## NOTE: (or rather questions) 
## - would this be better named leaf_reset_duration( )?... 
##   we are not really scaling.
## - should multipliers be retained in setting of new duration ?

def leaf_scale(dur, leaf):
   '''Example:
      
      >>> leaf_scale((5, 13), Note(0, (1, 8)))
      FixedDurationTuplet((5, 13), [Note(0, (1, 4))])'''

   assert isinstance(leaf, _Leaf) 
   assert isinstance(dur, Rational)
   assert dur > 0
   try:
      leaf.duration.written = dur
      return leaf
   except AssignabilityError:
      leaf.duration.written = _converge_to_power2(leaf.duration.written, dur)
      result = FixedDurationTuplet(dur, [leaf])
      return result


from abjad.tie.spanner import Tie
def leaf_scale_binary(dur, leaf):
   '''Example:
      
      >>> leaf_scale_binary((5, 16), Note(0, (1, 8)))
      [Note(0, (1, 4), Note(0, (1,16)]'''

   assert isinstance(leaf, _Leaf)
   assert isinstance(dur, Rational)
   assert dur > 0
   try:
      leaf.duration.written = dur
      return [leaf]
   except AssignabilityError:
      result = [ ]
      for wd in _duration_token_decompose(dur):
         l = copy_unspan([leaf])[0]
         l.duration.written = Rational(*wd)
         result.append(l)
      bequeath([leaf], result)
      ## tie leaves
      if not l.tie.parented:
         Tie(result)
      ## remove dynamics and articulations from tied leaves.
      for n in result[1:]:
         n.dynamics = None
         n.articulations = None
      ## remove afterGrace from all but the last leaf
      ## and Grace all but the first leaf
      for n in result[:-1]:
         n.grace.after = None
      for n in result[1:]:
         n.grace.before = None
      return result
