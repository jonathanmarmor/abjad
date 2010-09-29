from abjad.components._Component._Component import _Component
from abjad.components._Leaf._LeafDurationInterface import _LeafDurationInterface
from abjad.components._Leaf._LeafFormatter import _LeafFormatter
from abjad.tools.gracetools import Grace
import operator


class _Leaf(_Component):

   def __init__(self, duration):
      _Component.__init__(self)
      self._duration = _LeafDurationInterface(self, duration)
      self._formatter = _LeafFormatter(self)

   ## OVERLOADS ##

   def __and__(self, arg):
      return self._operate(arg, operator.__and__)
   
   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.duration.written == arg.duration.written:
            if self.duration.multiplier == arg.duration.multiplier:
               return True
      return False

   def __or__(self, arg):
      return self._operate(arg, operator.__or__)

   def __ne__(self, arg):
      return not self == arg

   def __str__(self):
      return self._compact_representation

   def __sub__(self, arg):
      return self._operate(arg, operator.__sub__)

   def __xor__(self, arg):
      return self._operate(arg, operator.__xor__)

   ## PRIVATE METHODS ##

   def _operate(self, arg, operator):
      assert isinstance(arg, _Leaf)
      from abjad.tools.leaftools._engender import _engender
      from abjad.tools import pitchtools
      self_pairs = set([
         x.pair for x in pitchtools.list_named_pitches_in_expr(self) if x is not None])
      arg_pairs = set([
         x.pair for x in pitchtools.list_named_pitches_in_expr(arg) if x is not None])
      pairs = operator(self_pairs, arg_pairs)
      return _engender(pairs, self.duration.written)

   ## PUBLIC ATTRIBUTES ##

   @property
   def after_grace(self):
      '''Read-only after grace music.
      '''
      if not hasattr(self, '_after_grace'):
         self._after_grace = Grace( )
         self._after_grace._carrier = self
         self._after_grace.kind = 'after'
      return self._after_grace

   @property
   def grace(self):
      '''Read-only grace music before leaf.
      '''
      if not hasattr(self, '_grace'):
         self._grace = Grace( )
         self._grace._carrier = self
      return self._grace
   
   @property
   def next(self):
      '''Read-only reference to next bead in thread.'''
      return self._navigator._next_bead

#   @property
#   def number(self):
#      '''Read-only number of `self` in thread.'''
#      return self._numbering._leaf

   @property
   def prev(self):
      '''Read-only reference to previous bead in thread.'''
      return self._navigator._prev_bead
