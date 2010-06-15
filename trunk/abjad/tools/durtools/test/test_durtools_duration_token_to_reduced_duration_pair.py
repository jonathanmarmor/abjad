from abjad import *


def test_durtools_duration_token_to_reduced_duration_pair_01( ):

   assert durtools.duration_token_to_reduced_duration_pair(Rational(1, 4)) == (1, 4)
   assert durtools.duration_token_to_reduced_duration_pair((1, 4)) == (1, 4)
   assert durtools.duration_token_to_reduced_duration_pair([1, 4]) == (1, 4)
   assert durtools.duration_token_to_reduced_duration_pair((2, )) == (2, 1)
   assert durtools.duration_token_to_reduced_duration_pair([2]) == (2, 1)
   assert durtools.duration_token_to_reduced_duration_pair(2) == (2, 1)
   assert durtools.duration_token_to_reduced_duration_pair('8.') == (3, 16)
