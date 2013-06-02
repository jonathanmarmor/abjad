from abjad.tools.stringtools.is_hyphen_delimited_lowercase_string import hyphen_delimited_lowercase_regex_body
import re


hyphen_delimited_lowercase_file_name_regex_body = """
    %s
    (\.[a-z,0-9]+)?
    """ % hyphen_delimited_lowercase_regex_body

hyphen_delimited_lowercase_file_name_regex = re.compile('^%s$' %
    hyphen_delimited_lowercase_file_name_regex_body, re.VERBOSE)

def is_hyphen_delimited_lowercase_file_name(expr):
    r'''.. versionadded:: 2.13

    True when `expr` is a string and is hyphen-delimited lowercase file name with extension::

        >>> stringtools.is_hyphen_delimited_lowercase_file_name('foo-bar')
        True

    False otherwise::

        >>> stringtools.is_hyphen_delimited_lowercase_file_name('foo.bar.blah')
        False

    Return boolean.
    '''

    if not isinstance(expr, str):
        return False

    if expr == '':
        return True

    return bool(hyphen_delimited_lowercase_file_name_regex.match(expr))