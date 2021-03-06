# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class InteractiveEditor(ScoreManagerObject):

    ### INITIALIZER ###

    def __init__(self, session=None, target=None):
        ScoreManagerObject.__init__(self, session=session)
        if target is not None:
            assert isinstance(target, self.target_class)
        self.target = target
        self.initialize_attributes_in_memory()
        if not hasattr(self, 'target_manifest'):
            raise Exception(self)
        self.explicit_breadcrumb = None

    ### SPECIAL METHODS ###

    def __repr__(self):
        if self.target is None:
            summary = ''
        else:
            summary = 'target={!r}'.format(self.target)
        return '{}({})'.format(type(self).__name__, summary)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        if self.explicit_breadcrumb:
            return self.explicit_breadcrumb
        elif self.target_name:
            return self.target_name
        else:
            return self.space_delimited_lowercase_target_class_name

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        attribute_name = self.target_manifest.menu_key_to_attribute_name(
            result)
        prepopulated_value = self.menu_key_to_prepopulated_value(result)
        kwargs = self.menu_key_to_delegated_editor_kwargs(result)
        editor = self.target_manifest.menu_key_to_editor(
            result, 
            session=self.session, 
            prepopulated_value=prepopulated_value, 
            **kwargs
            )
        if editor is not None:
            result = editor._run()
            if self.session.backtrack():
                self.is_autoadvancing = False
                return
            if hasattr(editor, 'target'):
                attribute_value = editor.target
            else:
                attribute_value = result
            self.set_target_attribute(attribute_name, attribute_value)

    def _make_main_menu(self):
        main_menu = self.session.io_manager.make_menu(where=self._where)
        keyed_attribute_section = \
            main_menu.make_keyed_attribute_section(
            is_numbered=True,
            ) 
        menu_entries = self.target_attribute_tokens
        keyed_attribute_section.menu_entries = menu_entries
        main_menu.hidden_section.append(('done', 'done'))
        return main_menu

    def _run(
        self, 
        breadcrumb=None, 
        cache=False, 
        clear=True, 
        is_autoadding=False,
        is_autoadvancing=False, 
        is_autostarting=False, 
        pending_user_input=None,
        ):
        self.session.io_manager._assign_user_input(pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        self.session.push_breadcrumb(self._breadcrumb)
        with self.backtracking:
            self.initialize_target()
        self.session.pop_breadcrumb()
        if self.session.backtrack():
            self.session.restore_breadcrumbs(cache=cache)
            return
        result = None
        entry_point = None
        self.is_autoadvancing = is_autoadvancing
        is_first_pass = True
        if is_autoadding:
            self.session.is_autoadding = True
        while True:
            breadcrumb = breadcrumb or self._breadcrumb
            self.session.push_breadcrumb(breadcrumb=breadcrumb)
            if self.session.is_autoadding:
                menu = self._make_main_menu()
                result = 'add'
                menu._run(
                    clear=clear, 
                    predetermined_user_input=result,
                    )
                is_first_pass = False
            elif is_first_pass and is_autostarting:
                menu = self._make_main_menu()
                result = menu._first_nonhidden_return_value_in_menu
                menu._run(
                    clear=clear, 
                    predetermined_user_input=result,
                    )
                is_first_pass = False
            elif result and self.is_autoadvancing:
                entry_point = entry_point or result
                result = menu._return_value_to_next_return_value_in_section(
                    result)
                if result == entry_point:
                    self.is_autoadvancing = False
                    self.session.pop_breadcrumb()
                    continue
            else:
                menu = self._make_main_menu()
                result = menu._run(clear=clear)
                if self.session.backtrack():
                    break
                elif not result:
                    self.session.pop_breadcrumb()
                    continue
            if result == 'done':
                break
            self._handle_main_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.is_autoadding = False
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)
        self.clean_up_attributes_in_memory()

    ### PUBLIC PROPERTIES ###

    @property
    def TargetManifest(self):
        from scoremanager import editors
        return editors.TargetManifest

    @property
    def attributes_in_memory(self):
        return self._attributes_in_memory

    @property
    def has_target(self):
        return self.target is not None

    @property
    def space_delimited_lowercase_target_class_name(self):
        return stringtools.string_to_space_delimited_lowercase(
            self.target_class.__name__)

    @property
    def target_attribute_names(self):
        result = []
        if hasattr(self, 'target_manifest'):
            result.extend(self.target_manifest.attribute_names)
        return result

    @property
    def target_attribute_tokens(self):
        if hasattr(self, 'target_manifest'):
            return self.make_target_attribute_tokens_from_target_manifest()
        else:
            raise ValueError

    @property
    def target_class(self):
        return self.target_manifest.target_class

    @property
    def target_keyword_attribute_names(self):
        result = []
        if hasattr(self, 'target_manifest'):
            result.extend(self.target_manifest.keyword_attribute_names)
        return result

    @property
    def target_name(self):
        target_name_attribute = self.target_manifest.target_name_attribute
        if target_name_attribute:
            return getattr(
                self.target, 
                self.target_manifest.target_name_attribute, 
                None)

    @property
    def target_positional_initializer_argument_names(self):
        result = []
        if hasattr(self, 'target_manifest'):
            result.extend(
                self.target_manifest.positional_initializer_argument_names)
        return result

    @property
    def target_positional_initializer_retrievable_attribute_names(self):
        result = []
        if hasattr(self, 'target_manifest'):
            result.extend(
                self.target_manifest.positional_initializer_retrievable_attribute_names)
        return result

    @property
    def target_summary_lines(self):
        result = []
        if self.target is not None:
            for target_attribute_name in self.target_attribute_names:
                name = stringtools.string_to_space_delimited_lowercase(
                    target_attribute_name)
                value = self.session.io_manager._get_one_line_menuing_summary(
                    getattr(self.target, target_attribute_name))
                result.append('{}: {}'.format(name, value))
        return result

    ### PUBLIC METHODS ###

    def attribute_name_to_menu_key(self, attribute_name, menu_keys):
        found_menu_key = False
        attribute_parts = attribute_name.split('_')
        i = 1
        while True:
            menu_key = ''.join([part[:i] for part in attribute_parts])
            if menu_key not in menu_keys:
                break
            i = i + 1
        return menu_key

    def clean_up_attributes_in_memory(self):
        if self.target is None:
            try:
                self.initialize_target_from_attributes_in_memory()
            except ValueError:
                pass
        self.initialize_attributes_in_memory()

    def copy_target_attributes_to_memory(self):
        self.initialize_attributes_in_memory()
        for attribute_name in \
            self.target_positional_initializer_retrievable_attribute_names:
            attribute_value = getattr(self.target, attribute_name, None)
            if attribute_value is not None:
                attribute_name = \
                    self.target_manifest.change_retrievable_attribute_name_to_initializer_argument_name(
                    attribute_name)
                self.attributes_in_memory[attribute_name] = attribute_value
        for attribute_name in self.target_keyword_attribute_names:
            attribute_value = getattr(self.target, attribute_name, None)
            if attribute_value is not None:
                self.attributes_in_memory[attribute_name] = attribute_value
        self.target = None

    def initialize_attributes_in_memory(self):
        self._attributes_in_memory = {}

    def initialize_target(self):
        if self.target is not None:
            return
        try:
            self.target = self.target_class()
        except:
            pass

    def initialize_target_from_attributes_in_memory(self):
        args, kwargs = [], {}
        for attribute_name in \
            self.target_positional_initializer_argument_names:
            if attribute_name in self.attributes_in_memory:
                args.append(self.attributes_in_memory.get(attribute_name))
        for attribute_name in self.target_keyword_attribute_names:
            if attribute_name in self.attributes_in_memory:
                kwargs[attribute_name] = \
                    self.attributes_in_memory.get(attribute_name)
        try:
            self.target = self.target_class(*args, **kwargs)
        except:
            pass

    def make_target_attribute_tokens_from_target_manifest(self):
        result = []
        for attribute_detail in self.target_manifest.attribute_details:
            if attribute_detail.is_null:
                result.append(())
                continue
            key = attribute_detail.menu_key
            display_string = attribute_detail._space_delimited_lowercase_name
            if self.target is not None:
                attribute_value = getattr(
                    self.target, attribute_detail.retrievable_name, None)
                if attribute_value is None:
                    attribute_value = getattr(
                        self.target, attribute_detail.name, None)
            else:
                attribute_value = self.attributes_in_memory.get(
                    attribute_detail.retrievable_name)
                if attribute_value is None:
                    attribute_value = self.attributes_in_memory.get(
                        attribute_detail.name)
            if hasattr(attribute_value, '__len__') and \
                not len(attribute_value):
                attribute_value = None
            prepopulated_value = self.session.io_manager._get_one_line_menuing_summary(
                attribute_value)
            menu_entry = (display_string, key, prepopulated_value)
            result.append(menu_entry)
        return result

    def menu_key_to_delegated_editor_kwargs(self, menu_key):
        return {}

    def menu_key_to_prepopulated_value(self, menu_key):
        attribute_name = \
            self.target_manifest.menu_key_to_attribute_name(menu_key)
        return getattr(self.target, attribute_name, None)

    def set_target_attribute(self, attribute_name, attribute_value):
        if self.target is not None:
            if not self.session.is_complete:
                # if the attribute is read / write
                try:
                    setattr(self.target, attribute_name, attribute_value)
                # elif the attribute is read-only
                except AttributeError:
                    self.copy_target_attributes_to_memory()
                    self.attributes_in_memory[attribute_name] = attribute_value
        else:
            self.attributes_in_memory[attribute_name] = attribute_value

    def target_args_to_target_summary_lines(self, target):
        result = []
        for arg in getattr(target, 'args', []):
            name = stringtools.string_to_space_delimited_lowercase(arg)
            value = self.session.io_manager._get_one_line_menuing_summary(getattr(target, arg))
            result.append('{}: {}'.format(name, value))
        return result

    def target_kwargs_to_target_summary_lines(self, target):
        result = []
        for kwarg in getattr(target, 'kwargs', []):
            name = stringtools.string_to_space_delimited_lowercase(kwarg)
            value = self.session.io_manager._get_one_line_menuing_summary(
                getattr(target, kwarg))
            result.append('{}: {}'.format(name, value))
        return result
