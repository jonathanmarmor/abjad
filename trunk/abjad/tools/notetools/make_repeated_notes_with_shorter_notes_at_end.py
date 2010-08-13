from abjad.components.Note import Note
from abjad.core import Rational
from abjad.tools.notetools.make_notes import make_notes


def make_repeated_notes_with_shorter_notes_at_end(pitch, written_duration, total_duration, 
   prolation = Rational(1)):
   r'''Construct notes with `pitch` and `written_duration`
   summing to `total_duration` under `prolation`::

      abjad> voice = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Rational(1, 16), Rational(4, 16)))
      abjad> f(voice)
      \new Voice {
         c'16
         c'16
         c'16
         c'16
      }

   Fill binary remaining duration with binary notes 
   of lesser written duration::

      abjad> voice = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Rational(1, 16), Rational(9, 32)))
      abjad> f(voice)
      \new Voice {
         c'16
         c'16
         c'16
         c'16
         c'32
      }

   Fill nonbinary remaining duration with ad hoc tuplet::

      abjad> voice = Voice(notetools.make_repeated_notes_with_shorter_notes_at_end(0, Rational(1, 16), Rational(4, 10)))
      abjad> f(voice)
      \new Voice {
         c'16
         c'16
         c'16
         c'16
         c'16
         c'16
         \times 4/5 {
            c'32
         }
      }

   Set `prolation` when constructing notes in a nonbinary measure.

   .. versionchanged:: 1.1.2
      renamed ``construct.note_train( )`` to
      ``notetools.make_repeated_notes_with_shorter_notes_at_end( )``.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.make_repeated_notes_with_shorter_notes_at_end( )`` to
      ``notetools.make_repeated_notes_with_shorter_notes_at_end( )``.
   '''

   prolated_duration = prolation * written_duration 
   current_duration = Rational(0)
   result = [ ]
   while current_duration + prolated_duration <= total_duration:
      result.append(Note(pitch, written_duration))
      current_duration += prolated_duration
   remainder_duration = total_duration - current_duration
   if Rational(0) < remainder_duration:
      #multiplied_remainder = ~prolation * remainder_duration
      multiplied_remainder = remainder_duration / prolation
      result.extend(make_notes(pitch, [multiplied_remainder]))
   return result
