# -*- encoding: utf-8 -*-
import os
import re


class PersistenceAgent(object):
    r'''A wrapper around Abjad's object persistence mechanisms.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> persist(staff).as_pdf('~/example.pdf') # doctest: +SKIP

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_client',
        )

    ### INITIALIZER ###

    def __init__(self, client):
        self._client = client

    ### SPECIAL METHODS ###

    def __repr__(self):
        '''Interpreter representation of persistence agent.

        ..  container:: example

            ::

                >>> staff = Staff("c'4 e'4 d'4 f'4")
                >>> persist(staff)
                PersistenceAgent(Staff{4})

        Returns string.
        '''
        return '{}({!s})'.format(
            type(self).__name__,
            self._client,
            )

    ### PUBLIC METHODS ###

    def as_ly(self, ly_filename=None):
        r'''Persists client as LilyPond file.

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>>  persist(staff).as_ly('~/example.ly') # doctest: +SKIP
            ('/Users/josiah/Desktop/test.ly', 0.04491996765136719)

        Return output path and elapsed formatting time.
        '''
        from abjad import abjad_configuration
        from abjad.tools import systemtools
        # get the illustration
        assert '__illustrate__' in dir(self._client)
        illustration = self._client.__illustrate__()
        # validate the output path
        if ly_filename is None:
            ly_filename = systemtools.IOManager.get_next_output_file_name()
            ly_filepath = os.path.join(
                abjad_configuration.abjad_output_directory_path,
                ly_filename,
                )
        else:
            ly_filepath = os.path.expanduser(ly_filename)
        assert ly_filepath.endswith('.ly')
        # format the illustration
        timer = systemtools.Timer()
        with timer:
            lilypond_format = format(illustration, 'lilypond')
        abjad_formatting_time = timer.elapsed_time
        # write the formatted illustration to disk
        with open(ly_filepath, 'w') as file_handle:
            file_handle.write(lilypond_format)
        return ly_filepath, abjad_formatting_time

    def as_module(self, module_filename, object_name):
        r'''Persists client as Python module.

        ::

            >>> inventory = timespantools.TimespanInventory([
            ...     timespantools.Timespan(0, 1),
            ...     timespantools.Timespan(2, 4),
            ...     timespantools.Timespan(6, 8),
            ...     ])
            >>> persist(inventory).as_module( # doctest: +SKIP
            ...     '~/example.py', 'inventory')

        '''
        assert '_storage_format' in dir(self._client)
        result = ['# -*- encoding: utf-8 -*-']
        storage_pieces = format(self._client, 'storage').splitlines()
        pattern = re.compile(r'\b[a-z]+tools\b')
        tools_package_names = set()
        for line in storage_pieces:
            match = pattern.search(line)
            while match is not None:
                group = match.group()
                tools_package_names.add(group)
                end = match.end()
                match = pattern.search(line, pos=end)
        for name in sorted(tools_package_names):
            result.append('from abjad.tools import {}'.format(name))
        result.append('')
        result.append('')
        result.append('{} = {}'.format(object_name, storage_pieces[0]))
        result.extend(storage_pieces[1:])
        result = '\n'.join(result)
        with open(os.path.expanduser(module_filename), 'w') as f:
            f.write(result)

    def as_pdf(self, pdf_filename=None):
        r'''Persists client as PDF.

        ::

            >>> staff = Staff("c'4 e'4 d'4 f'4")
            >>> persist(staff).as_pdf('~/example.pdf') # doctest: +SKIP
            ('/Users/josiah/Desktop/test.pdf', 0.047142982482910156, 0.7839350700378418)

        Return output path, elapsed formatting time and elapsed rendering time.
        '''
        from abjad.tools import systemtools
        assert '__illustrate__' in dir(self._client)
        # validate the output path
        if pdf_filename is not None:
            pdf_filepath = os.path.expanduser(pdf_filename)
            ly_filepath = '{}.ly'.format(os.path.splitext(pdf_filepath)[0])
        # format and write the lilypond file
        ly_filepath, abjad_formatting_time = self.as_ly(ly_filepath)
        pdf_filepath = '{}.pdf'.format(os.path.splitext(ly_filepath)[0])
        # render the pdf
        timer = systemtools.Timer()
        with timer:
            systemtools.IOManager.run_lilypond(ly_filepath)
        lilypond_rendering_time = timer.elapsed_time
        return pdf_filepath, abjad_formatting_time, lilypond_rendering_time