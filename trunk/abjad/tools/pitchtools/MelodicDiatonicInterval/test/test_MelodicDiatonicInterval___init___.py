from abjad import *


def test_MelodicDiatonicInterval___init____01( ):
   '''Can init from quality string and interval number.'''

   mdi = pitchtools.MelodicDiatonicInterval('major', 3)
   assert mdi.quality_string == 'major'
   assert mdi.number == 3



def test_MelodicDiatonicInterval___init____02( ):
   '''Can init from other melodic diatonic interval instance.'''

   mdi = pitchtools.MelodicDiatonicInterval('major', 3)
   new = pitchtools.MelodicDiatonicInterval(mdi)

   assert mdi.quality_string == 'major'
   assert mdi.number == 3

   assert new.quality_string == 'major'
   assert new.number == 3

   assert new is not mdi
   assert new == mdi
