from abjad import *


def test_DynamicTextSpanner_grob_handling_01( ):

   t = Voice(macros.scale(4))
   BeamSpanner(t[:])
   p = DynamicTextSpanner(t[:], 'f')
   p.override.dynamic_text.thickness = 3

   r'''
   \new Voice {
      \override DynamicText #'thickness = #3
      c'8 [ \f
      d'8
      e'8
      f'8 ]
      \revert DynamicText #'thickness
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Voice {\n\t\\override DynamicText #'thickness = #3\n\tc'8 [ \\f\n\td'8\n\te'8\n\tf'8 ]\n\t\\revert DynamicText #'thickness\n}"
