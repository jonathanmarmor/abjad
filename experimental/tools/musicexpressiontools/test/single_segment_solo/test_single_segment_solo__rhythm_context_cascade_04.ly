\context Score = "Grouped Rhythmic Staves Score" <<
	\context TimeSignatureContext = "TimeSignatureContext" {
		{
			\time 4/8
			s1 * 1/2
		}
		{
			\time 3/8
			s1 * 3/8
		}
		{
			\time 2/8
			s1 * 1/4
		}
	}
	\context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
		\context RhythmicStaff = "Staff 1" {
			\context Voice = "Voice 1" {
				{
					r8.
				}
				{
					r8.
				}
				{
					r8.
				}
				{
					r8.
				}
				{
					r8.
				}
				{
					r8.
				}
			}
		}
	>>
>>