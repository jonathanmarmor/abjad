from abjad import *
import py.test


def test_dfs_unique_left_01( ):
   '''
   Unique left-to-right DFS on a single note.
   '''

   t = Note(0, (1, 8))
   #g = t._navigator._DFSUniqueLeft( )
   g = t._navigator._DFS( )

   r'''
   c'4
   '''

   assert g.next( ) is t   
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Note(c', 8)
   '''


def test_dfs_unique_left_02( ):
   '''
   Unique left-to-right DFS on an empty container.
   '''

   t = Sequential([ ])
   #g = t._navigator._DFSUniqueLeft( )
   g = t._navigator._DFS( )

   r'''
   {
   }
   '''

   assert g.next( ) is t   
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Sequential( )
   '''


def test_dfs_unique_left_03( ):
   '''
   Unique left-to-right DFS on a flat container.
   '''

   t = Sequential(run(4))
   appictate(t)
   #g = t._navigator._DFSUniqueLeft( )
   g = t._navigator._DFS( )
   
   r'''
   {
      c'8
      cs'8
      d'8
      ef'8
   }
   '''

   assert g.next( ) is t
   assert g.next( ) is t[0]
   assert g.next( ) is t[1]
   assert g.next( ) is t[2]
   assert g.next( ) is t[3]
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Sequential(c'8, cs'8, d'8, ef'8)
   Note(c', 8)
   Note(cs', 8)
   Note(d', 8)
   Note(ef', 8)
   '''


def test_dfs_unique_left_04( ):
   '''
   Unique left-to-right DFS on nested container.
   '''

   t = Sequential(run(4))
   t.insert(2, Sequential(run(2)))
   appictate(t)
   #g = t._navigator._DFSUniqueLeft( )
   g = t._navigator._DFS( )

   r'''
   {
      c'8
      cs'8
      {
         d'8
         ef'8
      }
      e'8
      f'8
   }
   '''

   assert g.next( ) is t
   assert g.next( ) is t[0]
   assert g.next( ) is t[1]
   assert g.next( ) is t[2]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[3]
   assert g.next( ) is t[4]
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Sequential(c'8, cs'8, Sequential(d'8, ef'8), e'8, f'8)
   Note(c', 8)
   Note(cs', 8)
   Sequential(d'8, ef'8)
   Note(d', 8)
   Note(ef', 8)
   Note(e', 8)
   Note(f', 8)
   '''
