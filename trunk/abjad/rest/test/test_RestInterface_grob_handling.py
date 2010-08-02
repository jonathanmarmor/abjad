from abjad import *


def test_RestInterface_grob_handling_01( ):
   '''
   RestInterface handles the LilyPond Rest grob.
   '''

   t = Staff(macros.scale(4))
   t.rest.transparent = True

   r'''
   \new Staff \with {
           \override Rest #'transparent = ##t
   } {
           c'8
           d'8
           e'8
           f'8
   }
   '''
   
   assert t.format == "\\new Staff \\with {\n\t\\override Rest #'transparent = ##t\n} {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"


def test_RestInterface_grob_handling_02( ):
   '''
   Use clear to remove rest interace grob overrides.
   '''

   t = Staff(macros.scale(4))
   t.rest.transparent = True
   #t.rest.clear( )
   overridetools.clear_all_overrides_on_grob_handler(t.rest)

   r'''
   \new Staff {
           c'8
           d'8
           e'8
           f'8
   }
   '''
   
   assert t.format == "\\new Staff {\n\tc'8\n\td'8\n\te'8\n\tf'8\n}"
