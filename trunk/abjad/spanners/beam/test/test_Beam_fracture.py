from abjad import *


def test_Beam_fracture_01( ):
   '''This test shows that fracurting beyond the *first* leaf
      effectively does nothing except to replace an existing
      spanner with an identical new spanner.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   assert len(t.spanners.contained) == 1
   old = list(t.spanners.contained)[0]
   #assert old[ : ] == t[ : 4]
   assert old.components == tuple(t[ : 4])
   old.fracture(0, 'left')
   assert len(t.spanners.contained) == 1
   #new = list(t.spanners.contained)[0]
   #assert new[ : ] == old[ : ] == t[ : 4]
   #assert new.components == old.components == t[ : 4]
   #assert new != old


def test_Beam_fracture_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   assert len(t.spanners.contained) == 1
   old = list(t.spanners.contained)[0]
   #assert old[ : ] == t[ : 4]
   assert old.components == tuple(t[ : 4])
   old.fracture(1, 'left')
   assert len(t.spanners.contained) == 2
   #left, right = t.spanners.contained
   #assert left[ : ] == t[0 : 1]
   #assert left.components == t[0 : 1]
   #assert right[ : ] == t[1 : 4]
   #assert right.components == t[1 : 4]


def test_Beam_fracture_03( ):
   '''
   This test shows that fracurting beyond the *last* leaf
   effectively does nothing except to replace an existing
   spanner with an identical new spanner.
   '''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   assert len(t.spanners.contained) == 1
   old = list(t.spanners.contained)[0]
   #assert old[ : ] == t[ : 4]
   assert old.components == tuple(t[ : 4])
   old.fracture(-1, 'right')
   assert len(t.spanners.contained) == 1
   #new = list(t.spanners.contained)[0]
   #assert new[ : ] == old[ : ] == t[ : 4]
   #assert new.components == old.components == t[ : 4]
   #assert new != old


def test_Beam_fracture_04( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   assert len(t.spanners.contained) == 1
   old = list(t.spanners.contained)[0]
   #assert old[ : ] == t[ : 4]
   assert old.components == tuple(t[ : 4])
   old.fracture(1, 'right')
   assert len(t.spanners.contained) == 2
   #left, right = t.spanners.contained
   #assert left[ : ] == t[0 : 2]
   #assert left.components == t[0 : 2]
   #assert right[ : ] == t[2 : 4]
   #assert right.components == t[2 : 4]


def test_Beam_fracture_05( ):
   '''
   Fracture "both" fractures around leaf.
   '''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 5])
   old = list(t.spanners.contained)[0]
   old.fracture(2, 'both')
   assert len(t.spanners.contained) == 3
   #spanners = t.spanners.contained
   #assert len(spanners[0].components) == 2
   #assert len(spanners[1].components) == 1
   #assert len(spanners[2].components) == 2
   #assert spanners[0] != spanners[1] != spanners[2]
   assert len(t[0].beam.spanner) == 2
   assert len(t[2].beam.spanner) == 1
   assert len(t[3].beam.spanner) == 2
   assert t[0].beam.spanner != t[2].beam.spanner != t[3].beam.spanner
   componenttools.is_well_formed_component(t) ### check for Beam overlaps
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8 ]\n\td'8 [ ]\n\tef'8 [\n\te'8 ]\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''
   \new Staff {
           c'8 [
           cs'8 ]
           d'8 [ ]
           ef'8 [
           e'8 ]
           f'8
           fs'8
           g'8
   }
   '''


def test_Beam_fracture_06( ):
   '''
   Fracture "both" works of first spanned leaf.
   '''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 5])
   old = list(t.spanners.contained)[0]
   old.fracture(0, 'both')
   assert len(t.spanners.contained) == 2
   #spanners = list(t.spanners.contained)
   #assert len(spanners[0]) == 1
   #assert len(spanners[1]) == 4
   #assert spanners[0] != spanners[1] 
   assert len(t[0].beam.spanner) == 1
   assert len(t[1].beam.spanner) == 4
   assert t[0].beam.spanner != t[1].beam.spanner
   componenttools.is_well_formed_component(t) ### check for Beam overlaps
   assert t.format == "\\new Staff {\n\tc'8 [ ]\n\tcs'8 [\n\td'8\n\tef'8\n\te'8 ]\n\tf'8\n\tfs'8\n\tg'8\n}"
   r'''
   \new Staff {
           c'8 [ ]
           cs'8 [
           d'8
           ef'8
           e'8 ]
           f'8
           fs'8
           g'8
   }
   '''


def test_Beam_fracture_07( ):
   '''Fracture "both" works of last spanned leaf.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 5])
   old = list(t.spanners.contained)[0]
   old.fracture(4, 'both')
   assert len(t.spanners.contained) == 2
   #spanners = t.spanners.contained
   #assert len(spanners[0].components) == 4
   #assert len(spanners[1].components) == 1
   #assert spanners[0] != spanners[1] 
   assert len(t[0].beam.spanner) == 4
   assert len(t[4].beam.spanner) == 1
   assert t[0].beam.spanner != t[4].beam.spanner
   componenttools.is_well_formed_component(t) ### check for Beam overlaps
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8 [ ]\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''
   \new Staff {
           c'8 [
           cs'8
           d'8
           ef'8 ]
           e'8 [ ]
           f'8
           fs'8
           g'8
   }
   '''


def test_Beam_fracture_08( ):
   '''
   Fracture "both" works with negative indeces.
   '''

   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 5])
   old = list(t.spanners.contained)[0]
   old.fracture(-1, 'both')
   assert len(t.spanners.contained) == 2
   #spanners = t.spanners.contained
   #assert len(spanners[0].components) == 4
   #assert len(spanners[1].components) == 1
   #assert spanners[0] != spanners[1] 
   assert len(t[0].beam.spanner) == 4
   assert len(t[4].beam.spanner) == 1
   assert t[0].beam.spanner != t[4].beam.spanner
   componenttools.is_well_formed_component(t) ### check for Beam overlaps
   assert t.format == "\\new Staff {\n\tc'8 [\n\tcs'8\n\td'8\n\tef'8 ]\n\te'8 [ ]\n\tf'8\n\tfs'8\n\tg'8\n}"

   r'''
   \new Staff {
           c'8 [
           cs'8
           d'8
           ef'8 ]
           e'8 [ ]
           f'8
           fs'8
           g'8
   }
   '''
