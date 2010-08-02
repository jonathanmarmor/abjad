from abjad import *


def test_NoteHead___ne___01( ):
   '''Noteheads compare equal when note_head pitches compare equal.'''

   assert not NoteHead(None, 14) != NoteHead(None, 14)
   assert not NoteHead(None, Pitch('df', 5)) != NoteHead(None, Pitch('df', 5))


def test_NoteHead___ne___02( ):
   '''NoteHeads compare unequal when note_head pitches compare unequal.'''

   assert NoteHead(None, 14) != NoteHead(None, 15)
   assert NoteHead(None, Pitch('cs', 5)) != NoteHead(None, Pitch('df', 5))
