from abjad import *
import py.test


def test_beamtools_get_beam_spanner_attached_to_componnet_01( ):
   '''Get the only beam spanner attached to component.
   '''

   staff = Staff("c'8 d'8 e'8 f'8")
   beam = spannertools.BeamSpanner(staff.leaves)

   assert beamtools.get_beam_spanner_attached_to_component(staff[0]) is beam 
   assert beamtools.get_beam_spanner_attached_to_component(staff[1]) is beam 


def test_beamtools_get_beam_spanner_attached_to_componnet_02( ):
   '''Raise missing spanner error when no beam spanner attaches to component. 
   '''

   staff = Staff("c'8 d'8 e'8 f'8")

   assert py.test.raises(MissingSpannerError, 'beamtools.get_beam_spanner_attached_to_component(staff[0])')
   
   
def test_beamtools_get_beam_spanner_attached_to_componnet_03( ):
   '''Raise missing spanner error when no beam spanner attaches to component. 
   '''

   staff = Staff("c'8 d'8 e'8 f'8")
   spannertools.BeamSpanner(staff.leaves)
   spannertools.BeamSpanner(staff.leaves)
   
   assert py.test.raises(ExtraSpannerError, 'beamtools.get_beam_spanner_attached_to_component(staff[0])')
