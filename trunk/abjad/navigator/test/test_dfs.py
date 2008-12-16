from abjad import *
import py.test


### NOTE: all tests operate on the following expression ###

t = Voice(run(4))
t.insert(2, Parallel(Sequential(run(2)) * 2))
appictate(t)

r'''
   \new Voice {
      c'8
      cs'8
      <<
         {
            d'8
            ef'8
         }
         {
            e'8
            f'8
         }
      >>
      fs'8
      g'8
   }
'''


def test_dfs_default( ):
   '''
   Default depth-first search:
      * capped iteration returns no elements above self._client
      * unique returns each node at most once
      * no classes forbidden means all containers entered
   '''
  
   ### LEFT-TO-RIGHT ###

   g = t[2]._navigator._DFS( )

   assert g.next( ) is t[2]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2][0][0]
   assert g.next( ) is t[2][0][1]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2][1][0]
   assert g.next( ) is t[2][1][1]
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Sequential(d'8, ef'8)
   d'8
   ef'8
   Sequential(e'8, f'8)
   e'8
   f'8
   '''
   
   ### RIGHT-TO-LEFT ###

   g = t[2]._navigator._DFS(direction = 'right')

   assert g.next( ) is t[2]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2][1][1]
   assert g.next( ) is t[2][1][0]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2][0][1]
   assert g.next( ) is t[2][0][0]
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Sequential(e'8, f'8)
   f'8
   e'8
   Sequential(d'8, ef'8)
   ef'8
   d'8
   '''


def test_dfs_uncapped( ):
   '''
   Uncapped depth-first search:
      * uncapped iteration returns all elements above self._client
   '''
  
   ### LEFT-TO-RIGHT ###

   g = t[2]._navigator._DFS(capped = False)

   assert g.next( ) is t[2]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2][0][0]
   assert g.next( ) is t[2][0][1]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2][1][0]
   assert g.next( ) is t[2][1][1]
   assert g.next( ) is t
   assert g.next( ) is t[3]
   assert g.next( ) is t[4]
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Sequential(d'8, ef'8)
   d'8
   ef'8
   Sequential(e'8, f'8)
   e'8
   f'8
   Voice{5}
   fs'8
   g'8
   '''
   
   ### RIGHT-TO-LEFT ###

   g = t[2]._navigator._DFS(capped = False, direction = 'right')

   assert g.next( ) is t[2]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2][1][1]
   assert g.next( ) is t[2][1][0]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2][0][1]
   assert g.next( ) is t[2][0][0]
   assert g.next( ) is t
   assert g.next( ) is t[1]
   assert g.next( ) is t[0]
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Sequential(e'8, f'8)
   f'8
   e'8
   Sequential(d'8, ef'8)
   ef'8
   d'8
   Voice{5}
   cs'8
   c'8
   '''


def test_dfs_duplicates_allowed( ):
   '''
   Duplicates-allowed depth-first search:
      * nodes yield every time they are traversed
   '''
  
   ### LEFT-TO-RIGHT ###

   g = t[2]._navigator._DFS(unique = False)

   assert g.next( ) is t[2]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2][0][0]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2][0][1]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2][1][0]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2][1][1]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2]
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Sequential(d'8, ef'8)
   d'8
   Sequential(d'8, ef'8)
   ef'8
   Sequential(d'8, ef'8)
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Sequential(e'8, f'8)
   e'8
   Sequential(e'8, f'8)
   f'8
   Sequential(e'8, f'8)
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   '''
   
   ### RIGHT-TO-LEFT ###

   g = t[2]._navigator._DFS(unique = False, direction = 'right')

   assert g.next( ) is t[2]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2][1][1]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2][1][0]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2][0][1]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2][0][0]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2]
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Sequential(e'8, f'8)
   f'8
   Sequential(e'8, f'8)
   e'8
   Sequential(e'8, f'8)
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Sequential(d'8, ef'8)
   ef'8
   Sequential(d'8, ef'8)
   d'8
   Sequential(d'8, ef'8)
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   '''


def test_dfs_restricted( ):
   '''
   Restricted depth-first search:
      * iteration will yield -- but will not enter -- forbidden classes.
   '''

   ### LEFT-TO-RIGHT ###

   g = t._navigator._DFS(forbid = 'Parallel')

   assert g.next( ) is t
   assert g.next( ) is t[0]
   assert g.next( ) is t[1]
   assert g.next( ) is t[2]
   assert g.next( ) is t[3]
   assert g.next( ) is t[4]
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Voice{5}
   c'8
   cs'8
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   fs'8
   g'8
   '''
   
   ### RIGHT-TO-LEFT ###

   g = t._navigator._DFS(forbid = 'Parallel', direction = 'right')
   
   assert g.next( ) is t
   assert g.next( ) is t[4]
   assert g.next( ) is t[3]
   assert g.next( ) is t[2]
   assert g.next( ) is t[1]
   assert g.next( ) is t[0]
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Voice{5}
   g'8
   fs'8
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   cs'8
   c'8
   '''


def test_dfs_uncapped_and_duplicates_allowed( ):
   '''
   Uncapped depth-first search with duplicates allowed.
   '''

   ### LEFT-TO-RIGHT ###

   g = t[2]._navigator._DFS(capped = False, unique = False)

   assert g.next( ) is t[2]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2][0][0]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2][0][1]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2][1][0]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2][1][1]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2]
   assert g.next( ) is t
   assert g.next( ) is t[3]
   assert g.next( ) is t
   assert g.next( ) is t[4]
   assert g.next( ) is t
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Sequential(d'8, ef'8)
   d'8
   Sequential(d'8, ef'8)
   ef'8
   Sequential(d'8, ef'8)
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Sequential(e'8, f'8)
   e'8
   Sequential(e'8, f'8)
   f'8
   Sequential(e'8, f'8)
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Voice{5}
   fs'8
   Voice{5}
   g'8
   Voice{5}
   '''

   ### RIGHT-TO-LEFT ###

   g = t[2]._navigator._DFS(
      capped = False, unique = False, direction = 'right')

   assert g.next( ) is t[2]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2][1][1]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2][1][0]
   assert g.next( ) is t[2][1]
   assert g.next( ) is t[2]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2][0][1]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2][0][0]
   assert g.next( ) is t[2][0]
   assert g.next( ) is t[2]
   assert g.next( ) is t
   assert g.next( ) is t[1]
   assert g.next( ) is t
   assert g.next( ) is t[0]
   assert g.next( ) is t
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Sequential(e'8, f'8)
   f'8
   Sequential(e'8, f'8)
   e'8
   Sequential(e'8, f'8)
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Sequential(d'8, ef'8)
   ef'8
   Sequential(d'8, ef'8)
   d'8
   Sequential(d'8, ef'8)
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Voice{5}
   cs'8
   Voice{5}
   c'8
   Voice{5}
   '''


def test_dfs_uncapped_and_restricted( ):
   '''
   Uncapped and restricted depth-first search.
   '''

   ### LEFT-TO-RIGHT ###

   g = t[2]._navigator._DFS(capped = False, forbid = 'Parallel')
   
   assert g.next( ) is t[2]
   assert g.next( ) is t
   assert g.next( ) is t[3]
   assert g.next( ) is t[4]

   r'''
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Voice{5}
   fs'8
   g'8
   '''

   ### RIGHT-TO-LEFT ###
   
   g = t[2]._navigator._DFS(
      capped = False, forbid = 'Parallel', direction = 'right')

   assert g.next( ) is t[2]
   assert g.next( ) is t
   assert g.next( ) is t[1]
   assert g.next( ) is t[0]

   r'''
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Voice{5}
   cs'8
   c'8
   '''


def test_dfs_restricted_with_duplicates_allowed( ):
   '''
   Restricted depth-first search with duplicates allowed.
   '''

   ### LEFT-TO-RIGHT

   g = t._navigator._DFS(forbid = 'Parallel', unique = False)

   assert g.next( ) is t
   assert g.next( ) is t[0]
   assert g.next( ) is t
   assert g.next( ) is t[1]
   assert g.next( ) is t
   assert g.next( ) is t[2]
   assert g.next( ) is t
   assert g.next( ) is t[3]
   assert g.next( ) is t
   assert g.next( ) is t[4]
   assert g.next( ) is t
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Voice{5}
   c'8
   Voice{5}
   cs'8
   Voice{5}
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Voice{5}
   fs'8
   Voice{5}
   g'8
   Voice{5}
   '''

   ### RIGHT-TO-LEFT ###

   g = t._navigator._DFS(
      forbid = 'Parallel', unique = False, direction = 'right')

   assert g.next( ) is t
   assert g.next( ) is t[4]
   assert g.next( ) is t
   assert g.next( ) is t[3]
   assert g.next( ) is t
   assert g.next( ) is t[2]
   assert g.next( ) is t
   assert g.next( ) is t[1]
   assert g.next( ) is t
   assert g.next( ) is t[0]
   assert g.next( ) is t
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Voice{5}
   g'8
   Voice{5}
   fs'8
   Voice{5}
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Voice{5}
   cs'8
   Voice{5}
   c'8
   Voice{5}
   '''


def test_dfs_uncapped_and_restricted_with_duplicates_allowed( ):
   '''
   Uncapped but restricted depth-first serach with duplicates allowed.
   '''
  
   ### LEFT-TO-RIGHT ###

   g = t[2]._navigator._DFS(
      capped = False, forbid = 'Parallel', unique = False)

   assert g.next( ) is t[2]
   assert g.next( ) is t
   assert g.next( ) is t[3]
   assert g.next( ) is t
   assert g.next( ) is t[4]
   assert g.next( ) is t
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Voice{5}
   fs'8
   Voice{5}
   g'8
   Voice{5}
   '''

   ### RIGHT-TO-LEFT ###

   g = t[2]._navigator._DFS(
      capped = False, forbid = 'Parallel', unique = False, direction = 'right')

   assert g.next( ) is t[2]
   assert g.next( ) is t
   assert g.next( ) is t[1]
   assert g.next( ) is t
   assert g.next( ) is t[0]
   assert g.next( ) is t
   assert py.test.raises(StopIteration, 'g.next( )')

   r'''
   Parallel(Sequential(d'8, ef'8), Sequential(e'8, f'8))
   Voice{5}
   cs'8
   Voice{5}
   c'8
   Voice{5}
   '''
