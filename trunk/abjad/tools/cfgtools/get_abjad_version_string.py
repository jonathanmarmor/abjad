from abjad.cfg import cfg


def get_abjad_version_string( ):
   '''.. versionadded:: 1.1.2

   Get Abjad version string::

      abjad> cfgtools.get_abjad_version_string( )
      '1.1.2'

   Return string.
   '''

   return vars(cfg)['abjad_version_number']
