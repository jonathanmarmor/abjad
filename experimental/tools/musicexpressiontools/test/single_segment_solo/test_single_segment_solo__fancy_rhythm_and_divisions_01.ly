\context Score = "Grouped Rhythmic Staves Score" <<
	\context TimeSignatureContext = "TimeSignatureContext" {
		{
			\time 4/8
			s1 * 1/2
		}
		{
			s1 * 1/2
		}
		{
			s1 * 1/2
		}
	}
	\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
		\context RhythmicStaff = "Staff 1" {
			\context Voice = "Voice 1" {
				{
					s1 * 1/2
				}
				{
					s1 * 1/8
				}
				{
					\set stemLeftBeamCount = #0
					\set stemRightBeamCount = #3
					c'32 [
					\set stemLeftBeamCount = #3
					\set stemRightBeamCount = #1
					c'32
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #3
					c'32
					\set stemLeftBeamCount = #3
					\set stemRightBeamCount = #1
					c'32
				}
				{
					\set stemLeftBeamCount = #1
					\set stemRightBeamCount = #3
					c'32
					\set stemLeftBeamCount = #3
					\set stemRightBeamCount = #0
					c'32 ]
				}
				{
					s1 * 3/16
				}
				{
					s1 * 1/2
				}
			}
		}
	>>
>>