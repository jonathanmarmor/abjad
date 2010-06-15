from abjad import *


def test_durtools_rational_to_equal_or_greater_assignable_rational_01( ):
   '''Wrapper around durtools.rational_to_equal_or_greater_binary_rational( ) 
   that returns dotted and double dotted durations where appropriate.
   Note that output *does not* increase monotonically.'''

   assert durtools.rational_to_equal_or_greater_assignable_rational(
      Rational(1, 16)) == Rational(1, 16)
   assert durtools.rational_to_equal_or_greater_assignable_rational(
      Rational(2, 16)) == Rational(2, 16)
   assert durtools.rational_to_equal_or_greater_assignable_rational(
      Rational(3, 16)) == Rational(3, 16)
   assert durtools.rational_to_equal_or_greater_assignable_rational(
      Rational(4, 16)) == Rational(4, 16)
   assert durtools.rational_to_equal_or_greater_assignable_rational(
      #Rational(5, 16)) == Rational(8, 16)
      Rational(5, 16)) == Rational(6, 16)
   assert durtools.rational_to_equal_or_greater_assignable_rational(
      Rational(6, 16)) == Rational(6, 16)
   assert durtools.rational_to_equal_or_greater_assignable_rational(
      Rational(7, 16)) == Rational(7, 16)
   assert durtools.rational_to_equal_or_greater_assignable_rational(
      Rational(8, 16)) == Rational(8, 16)
   assert durtools.rational_to_equal_or_greater_assignable_rational(
      #Rational(9, 16)) == Rational(16, 16)
      Rational(9, 16)) == Rational(12, 16)
   assert durtools.rational_to_equal_or_greater_assignable_rational(
      #Rational(10, 16)) == Rational(16, 16)
      Rational(10, 16)) == Rational(12, 16)
   assert durtools.rational_to_equal_or_greater_assignable_rational(
      #Rational(11, 16)) == Rational(16, 16)
      Rational(11, 16)) == Rational(12, 16)
   assert durtools.rational_to_equal_or_greater_assignable_rational(
      Rational(12, 16)) == Rational(12, 16)
