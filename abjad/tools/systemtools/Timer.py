# -*- encoding: utf-8 -*-
import time
from abjad.tools.abctools import ContextManager


class Timer(ContextManager):
    r'''A timing context manager:

    ::

        >>> timer = systemtools.Timer()
        >>> with timer:
        ...     for _ in xrange(1000000):
        ...         x = 1 + 1
        ...
        >>> timer.elapsed_time # doctest: +SKIP
        0.092742919921875

    The timer can also be accessed from within the `with` block:

    ::

        >>> with systemtools.Timer() as timer: # doctest: +SKIP
        ...     for _ in range(5):
        ...         for _ in xrange(1000000):
        ...             x = 1 + 1
        ...         print timer.elapsed_time
        ...
        0.101150989532
        0.203935861588
        0.304930925369
        0.4057970047
        0.50649189949

    Timers can be reused between `with` blocks. They will reset their clock on
    entering any `with` block.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_start_time',
        '_stop_time',
        )

    ### INITIALIZER ###

    def __init__(self):
        self._start_time = None
        self._stop_time = None

    ### SPECIAL METHODS ###

    def __enter__(self):
        r'''Enters context manager.

        Returns context manager.
        '''
        self._stop_time = None
        self._start_time = time.time()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        r'''Exist context manager.

        Returns none.
        '''
        self._stop_time = time.time()

    ### PUBLIC PROPERTIES ###

    @property
    def elapsed_time(self):
        r'''Elapsed time.

        Return float or none.
        '''
        if self.start_time is not None:
            if self.stop_time is not None:
                return self.stop_time - self.start_time
            return time.time() - self.start_time
        return None

    @property
    def start_time(self):
        r'''Start time of timer.

        Returns time.
        '''
        return self._start_time

    @property
    def stop_time(self):
        r'''Stop time of timer.

        Returns time.
        '''
        return self._stop_time
