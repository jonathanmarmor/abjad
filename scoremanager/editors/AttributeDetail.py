# -*- encoding: utf-8 -*-
import types
from abjad.tools.abctools.AbjadObject import AbjadObject
from scoremanager.editors.InteractiveEditor import InteractiveEditor


class AttributeDetail(AbjadObject):

    ### INITIALIZER ###

    def __init__(self, *args, **kwargs):
        is_null = False
        if len(args) == 0:
            name = retrievable_name = _space_delimited_lowercase_name = \
                menu_key = editor_callable = is_positional = None
            is_null = True
        elif len(args) == 3:
            name, menu_key, editor_callable = args
            _space_delimited_lowercase_name = None
            is_positional = True
            retrievable_name = name
        elif len(args) == 4:
            name, _space_delimited_lowercase_name, menu_key, editor_callable = args
            is_positional = True
            retrievable_name = name
        elif len(args) == 5:
            name, _space_delimited_lowercase_name, menu_key, editor_callable, is_positional = args
            retrievable_name = name
        elif len(args) == 6:
            name, retrievable_name, _space_delimited_lowercase_name, \
                menu_key, editor_callable, is_positional = args
        else:
            message = 'can not parse attribute detail: {!r}.'
            message = message.format(args)
            raise ValueError(message)
        if not _space_delimited_lowercase_name and name:
            _space_delimited_lowercase_name = name.replace('_', ' ')
        self.name = name
        self.retrievable_name = retrievable_name
        self._space_delimited_lowercase_name = _space_delimited_lowercase_name
        self.menu_key = menu_key
        self.editor_callable = editor_callable
        self.is_positional = is_positional
        self.allow_none = kwargs.get('allow_none', True)
        self.is_null = is_null

    ### SPECIAL METHODS ###

    def __repr__(self):
        parts = [
            repr(self._space_delimited_lowercase_name),
            repr(self.menu_key),
            self.editor_callable.__name__]
        if not self.allow_none:
            parts.append('allow_none=False')
        parts = ', '.join(parts)
        return '{}({})'.format(type(self).__name__, parts)

    ### PUBLIC METHODS ###

    def get_editor(
        self, 
        space_delimited_attribute_name, 
        prepopulated_value, 
        session=None, 
        **kwargs
        ):
        from scoremanager import iotools
        from scoremanager import wizards
        if isinstance(self.editor_callable, types.FunctionType) and \
            self.editor_callable.__name__.startswith('make_'):
            editor = self.editor_callable(session=session, **kwargs)
        elif isinstance(self.editor_callable, types.FunctionType):
            editor = self.editor_callable(
                space_delimited_attribute_name,
                session=session, 
                prepopulated_value=prepopulated_value, 
                allow_none=self.allow_none, 
                **kwargs
                )
        elif issubclass(self.editor_callable, InteractiveEditor):
            editor = self.editor_callable(
                session=session, 
                target=prepopulated_value, 
                **kwargs
                )
        elif issubclass(self.editor_callable, iotools.Selector):
            editor = self.editor_callable(session=session, **kwargs)
        elif issubclass(self.editor_callable, wizards.Wizard):
            editor = self.editor_callable(
                session=session, target=prepopulated_value, **kwargs)
        else:
            message = 'what is {!r}?'
            message = message.format(self.editor_callable)
            raise ValueError(message)
        return editor
