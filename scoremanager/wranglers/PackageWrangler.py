# -*- encoding: utf-8 -*-
import os
from abjad.tools import sequencetools
from abjad.tools import stringtools
from scoremanager.wranglers.Wrangler import Wrangler


class PackageWrangler(Wrangler):
    r'''Package wrangler.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import managers
        asset_storehouse_filesystem_path_in_built_in_asset_library = \
            self.configuration.packagesystem_path_to_filesystem_path(
            self.asset_storehouse_packagesystem_path_in_built_in_asset_library)
        asset_storehouse_filesystem_path_in_user_asset_library = \
            self.configuration.packagesystem_path_to_filesystem_path(
            self.asset_storehouse_packagesystem_path_in_user_asset_library)
        self.asset_storehouse_filesystem_path_in_built_in_asset_library = \
            asset_storehouse_filesystem_path_in_built_in_asset_library
        self.asset_storehouse_filesystem_path_in_user_asset_library = \
            asset_storehouse_filesystem_path_in_user_asset_library
        Wrangler.__init__(self, session=session)
        self._asset_manager_class = managers.PackageManager

    ### PRIVATE PROPERTIES ###

    @property
    def _current_storehouse_packagesystem_path(self):
        if self.session.is_in_score:
            parts = []
            parts.append(self.session.current_score_package_path)
            parts.extend(self.score_package_asset_storehouse_path_infix_parts)
            return '.'.join(parts)
        else:
            return self.asset_storehouse_packagesystem_path_in_built_in_asset_library

    @property
    def _temporary_asset_manager(self):
        return self._initialize_asset_manager(
            self._temporary_asset_package_path)

    @property
    def _temporary_asset_name(self):
        return '__temporary_package'

    @property
    def _temporary_asset_package_path(self):
        if self._current_storehouse_packagesystem_path:
            return '.'.join([
                self._current_storehouse_packagesystem_path,
                self._temporary_asset_name])
        else:
            return self._temporary_asset_name

    ### PRIVATE METHODS ###

    def _handle_main_menu_result(self, result):
        self.session.io_manager.print_not_yet_implemented()

    def _initialize_asset_manager(self, packagesystem_path):
        if os.path.sep in packagesystem_path:
            pacakgesystem_path = \
            self.configuration.filesystem_path_to_packagesystem_path(
            packagesystem_path)
        return self._asset_manager_class(
            packagesystem_path=packagesystem_path, 
            session=self.session,
            )

    def _is_valid_directory_entry(self, expr):
        superclass = super(PackageWrangler, self)
        if superclass._is_valid_directory_entry(expr):
            if '.' not in expr:
                return True
        return False

    def _make_main_menu(self, head=None):
        self.session.io_manager.print_not_yet_implemented()

    def _make_asset_menu_entries(self, head=None):
        names = self.list_asset_names(head=head)
        keys = len(names) * [None]
        prepopulated_return_values = len(names) * [None]
        paths = self.list_visible_asset_packagesystem_paths(head=head)
        assert len(names) == len(keys) == len(paths)
        if names:
            sequences = (names, [None], [None], paths)
            entries = sequencetools.zip_sequences(sequences, cyclic=True)
            package_manager = self._get_current_package_manager()
            if package_manager:
                view_name = package_manager._get_metadatum('view_name')
                if view_name:
                    view_inventory = self._read_view_inventory_from_disk()
                    if view_inventory:
                        correct_view = view_inventory.get(view_name)
                        if correct_view:
                            entries = \
                                self._sort_asset_menu_entries_by_view(
                                entries,
                                correct_view,
                                )
            return entries

    @staticmethod
    def _sort_asset_menu_entries_by_view(entries, view):
        entries_found_in_view = len(entries) * [None]
        entries_not_found_in_view = []
        for entry in entries:
            name = entry[0]
            if name in view:
                index = view.index(name)
                entries_found_in_view[index] = entry
            else:
                entries_not_found_in_view.append(entry)
        entries_found_in_view = [
            x for x in entries_found_in_view 
            if not x is None
            ]
        sorted_entries = entries_found_in_view + entries_not_found_in_view
        assert len(sorted_entries) == len(entries)
        return sorted_entries

    ### PUBLIC METHODS ###

    def interactively_get_available_packagesystem_path(
        self, 
        pending_user_input=None,
        ):
        r'''Interactively gets available packagesystem path.

        Returns string.
        '''
        self.session.io_manager._assign_user_input(pending_user_input)
        while True:
            getter = self.session.io_manager.make_getter(where=self._where)
            getter.append_space_delimited_lowercase_string('name')
            with self.backtracking:
                package_name = getter._run()
            if self.session.backtrack():
                return
            package_name = \
                stringtools.string_to_accent_free_snake_case(package_name)
            package_path = '.'.join([
                self._current_storehouse_packagesystem_path, 
                package_name,
                ])
            if self.configuration.packagesystem_path_exists(package_path):
                line = 'Package {!r} already exists.'
                line = line.format(package_path)
                self.session.io_manager.display([line, ''])
            else:
                return package_path

    def interactively_make_asset(
        self,
        pending_user_input=None,
        ):
        r'''Interactively makes asset.

        Returns none.
        '''
        self.session.io_manager._assign_user_input(pending_user_input)
        with self.backtracking:
            package_path = \
                self.interactively_get_available_packagesystem_path()
        if self.session.backtrack():
            return
        self.make_asset(package_path)

    def interactively_rename_asset(
        self, 
        head=None,
        pending_user_input=None,
        ):
        r'''Interactively renames asset.

        Returns none.
        '''
        self.session.io_manager._assign_user_input(pending_user_input)
        with self.backtracking:
            asset_package_path = \
                self.interactively_select_asset_packagesystem_path(
                head=head, infinitival_phrase='to rename')
        if self.session.backtrack():
            return
        asset_manager = self._initialize_asset_manager(asset_package_path)
        asset_manager.interactively_rename()

    def interactively_select_asset_packagesystem_path(
        self,
        clear=True,
        cache=False,
        head=None,
        infinitival_phrase=None,
        pending_user_input=None,
        ):
        '''Interactively selects asset packagesystem path.

        Returns string.
        '''
        self.session.io_manager._assign_user_input(pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        while True:
            self.session.push_breadcrumb(
                self._make_asset_selection_breadcrumb(
                infinitival_phrase=infinitival_phrase))
            menu = self._make_asset_selection_menu(head=head)
            result = menu._run(clear=clear)
            if self.session.backtrack():
                break
            elif not result:
                self.session.pop_breadcrumb()
                continue
            else:
                break
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)
        return result

    def list_asset_managers(
        self,
        in_built_in_asset_library=True,
        in_user_asset_library=True,
        in_built_in_score_packages=True,
        in_user_score_packages=True,
        head=None,
        ):
        r'''Lists asset managers.

        Returns list.
        '''
        result = []
        for package_path in self.list_asset_packagesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head,
            ):
            asset_manager = self._initialize_asset_manager(package_path)
            result.append(asset_manager)
        return result

    def list_asset_packagesystem_paths(
        self,
        in_built_in_asset_library=True,
        in_user_asset_library=True,
        in_built_in_score_packages=True,
        in_user_score_packages=True,
        head=None,
        ):
        r'''Lists asset packagesystem paths.

        Returns list.
        '''
        result = []
        for filesystem_path in self.list_asset_filesystem_paths(
            in_built_in_asset_library=in_built_in_asset_library,
            in_user_asset_library=in_user_asset_library,
            in_built_in_score_packages=in_built_in_score_packages,
            in_user_score_packages=in_user_score_packages,
            head=head):
            packagesystem_path = \
                self.configuration.filesystem_path_to_packagesystem_path(
                    filesystem_path)
            result.append(packagesystem_path)
        return result

    def list_asset_storehouse_packagesystem_paths(
        self,
        in_built_in_asset_library=True,
        in_user_asset_library=True,
        in_built_in_score_packages=True,
        in_user_score_packages=True,
        ):
        r'''Lists asset storehouse packagesystem paths.

        Returns list.
        '''
        result = []
        superclass = super(PackageWrangler, self)
        for filesystem_path in \
            superclass.list_asset_storehouse_filesystem_paths(
            in_built_in_asset_library=True,
            in_user_asset_library=True,
            in_built_in_score_packages=True,
            in_user_score_packages=True,
            ):
            packagesystem_path = \
                self.configuration.filesystem_path_to_packagesystem_path(
                filesystem_path)
            result.append(packagesystem_path)
        return result

    def list_visible_asset_packagesystem_paths(self, head=None):
        r'''Lists visible asset packagesystem paths.

        Returns list.
        '''
        result = []
        if hasattr(self, 'list_visible_asset_managers'):
            for asset_manager in self.list_visible_asset_managers(head=head):
                result.append(asset_manager.package_path)
        else:
            for asset_manager in self.list_asset_managers(
                in_built_in_asset_library=True,
                in_user_asset_library=True,
                in_built_in_score_packages=True,
                in_user_score_packages=True,
                head=head,
                ):
                result.append(asset_manager.package_path)
        return result

    def make_asset(self, asset_name):
        r'''Makes asset.

        Returns none.
        '''
        assert stringtools.is_snake_case_package_name(asset_name)
        asset_filesystem_path = os.path.join(
            self._current_storehouse_filesystem_path, asset_name)
        os.mkdir(asset_filesystem_path)
        package_manager = self._initialize_asset_manager(asset_name)
        package_manager.interactively_fix(is_interactive=False)

    def make_asset_storehouse_packages(self, is_interactive=False):
        r'''Makes asset storehouse packages.

        Returns none.
        '''
        for package_path in self.list_asset_storehouse_packagesystem_paths(
            in_built_in_asset_library=True,
            in_user_asset_library=True,
            in_built_in_score_packages=True,
            in_user_score_packages=True,
            ):
            self.make_empty_package(package_path)
        self.session.io_manager.proceed(
            'missing packages created.', 
            is_interactive=is_interactive,
            )

    def make_empty_package(self, package_path):
        r'''Makes empty package.

        Returns none.
        '''
        if package_path is None:
            return
        directory_path = \
            self.configuration.packagesystem_path_to_filesystem_path(
            package_path)
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
            initializer_file_path = os.path.join(
                directory_path, '__init__.py')
            file_reference = file(initializer_file_path, 'w')
            file_reference.write('')
            file_reference.close()

    ### UI MANIFEST ###

    user_input_to_action = Wrangler.user_input_to_action.copy()
    user_input_to_action.update({
        'missing': make_asset_storehouse_packages,
        'new': interactively_make_asset,
        'ren': interactively_rename_asset,
        })
