# -*- encoding: utf-8 -*-
import os
import subprocess
from scoremanager.core.ScoreManagerObject import ScoreManagerObject


class ScoreManager(ScoreManagerObject):
    r'''Score manager.

    ::

        >>> score_manager = scoremanager.core.ScoreManager()
        >>> score_manager
        ScoreManager()

    Returns score manager.
    '''

    ### INITIALIZER ###

    def __init__(self, session=None):
        from scoremanager import wranglers
        ScoreManagerObject.__init__(self, session=session)
        self._segment_package_wrangler = \
            wranglers.SegmentPackageWrangler(session=self.session)
        self._material_package_manager_wrangler = \
            wranglers.MaterialPackageManagerWrangler(session=self.session)
        self._material_package_wrangler = \
            wranglers.MaterialPackageWrangler(session=self.session)
        self._score_package_wrangler = \
            wranglers.ScorePackageWrangler(session=self.session)
        self._stylesheet_file_wrangler = \
            wranglers.StylesheetFileWrangler(session=self.session)

    ### PRIVATE PROPERTIES ###

    @property
    def _breadcrumb(self):
        return 'score manager'

    @property
    def _score_status_string(self):
        return '{} scores'.format(self.session.scores_to_show)

    ### PRIVATE METHODS ###

    def _get_next_score_package_name(self):
        score_package_names = self.score_package_wrangler.list_asset_names()
        if self.session.snake_case_current_score_name is None:
            return score_package_names[0]
        index = score_package_names.index(
            self.session.snake_case_current_score_name)
        next_index = (index + 1) % len(score_package_names)
        return score_package_names[next_index]

    def _get_previous_score_package_name(self):
        score_package_names = self.score_package_wrangler.list_asset_names()
        if self.session.snake_case_current_score_name is None:
            return score_package_names[-1]
        index = score_package_names.index(
            self.session.snake_case_current_score_name)
        prev_index = (index - 1) % len(score_package_names)
        return score_package_names[prev_index]

    def _handle_main_menu_result(self, result):
        if result in self.user_input_to_action:
            self.user_input_to_action[result](self)
        else:
            wrangler = self.score_package_wrangler
            if result in wrangler.list_visible_asset_packagesystem_paths():
                self.interactively_edit_score(result)

    def _handle_repository_menu_result(self, result):
        r'''Returns true to exit the repository menu.
        '''
        this_result = False
        if result == 'add':
            self.score_package_wrangler.repository_add_assets()
        elif result == 'ci':
            self.score_package_wrangler.repository_ci_assets()
        elif result == 'st':
            self.score_package_wrangler.repository_st_assets()
        elif result == 'up':
            self.score_package_wrangler.repository_up_assets()
            return True
        return this_result

    def _make_main_menu(self):
        menu = self._make_score_selection_menu()
        command_section = menu.make_command_section()
        command_section.append(('materials', 'm'))
        command_section.append(('stylesheets', 'y'))
        command_section.append(('new score', 'new'))
        hidden_section = menu.make_command_section(is_hidden=True)
        hidden_section.append(('scores - fix', 'fix'))
        hidden_section.append(('scores - profile', 'profile'))
        hidden_section.append(('scores - test', 'test'))
        hidden_section = menu.make_command_section(is_hidden=True)
        hidden_section.append(('show - active scores', 'active'))
        hidden_section.append(('show - all score', 'all'))
        hidden_section.append(('show - mothballed scores', 'mothballed'))
        hidden_section = menu.make_command_section(is_hidden=True)
        hidden_section.append(('work with repository', 'rep'))
        hidden_section.append(('write cache', 'wc'))
        return menu

    def _make_repository_menu(self):
        menu = self.session.io_manager.make_menu(where=self._where)
        command_section = menu.make_command_section()
        command_section.append(('add', 'add'))
        command_section.append(('commit', 'ci'))
        command_section.append(('status', 'st'))
        command_section.append(('update', 'up'))
        return menu

    def _make_score_selection_menu(self):
        if self.session.is_first_run:
            if hasattr(self, 'start_menu_entries'):
                menu_entries = self.start_menu_entries
            else:
                self.write_cache()
                menu_entries = \
                    self.score_package_wrangler._make_asset_menu_entries()
            self.session.is_first_run = False
        else:
            menu_entries = \
                self.score_package_wrangler._make_asset_menu_entries()
        menu = self.session.io_manager.make_menu(where=self._where)
        asset_section = menu.make_asset_section()
        asset_section.menu_entries = menu_entries
        return menu

    def _run(
        self, 
        pending_user_input=None, 
        clear=True, 
        cache=False, 
        is_test=False, 
        dump_transcript=False,
        ):
        type(self).__init__(self)
        self.session.io_manager._assign_user_input(
            pending_user_input=pending_user_input)
        self.session.cache_breadcrumbs(cache=cache)
        self.session.push_breadcrumb(self._breadcrumb)
        if is_test:
            self.session.is_test = True
        self.session.dump_transcript = dump_transcript
        run_main_menu = True
        while True:
            self.session.push_breadcrumb(self._score_status_string)
            if run_main_menu:
                menu = self._make_main_menu()
                result = menu._run(clear=clear)
            else:
                run_main_menu = True
            if self.session.backtrack(source='home'):
                self.session.pop_breadcrumb()
                self.session.clean_up()
                break
            elif self.session.is_navigating_to_next_score:
                self.session.is_navigating_to_next_score = False
                self.session.is_backtracking_to_score_manager = False
                result = self._get_next_score_package_name()
            elif self.session.is_navigating_to_previous_score:
                self.session.is_navigating_to_previous_score = False
                self.session.is_backtracking_to_score_manager = False
                result = self._get_previous_score_package_name()
            elif not result:
                self.session.pop_breadcrumb()
                continue
            self._handle_main_menu_result(result)
            if self.session.backtrack(source='home'):
                self.session.pop_breadcrumb()
                self.session.clean_up()
                break
            elif self.session.is_navigating_to_sibling_score:
                run_main_menu = False
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()
        self.session.restore_breadcrumbs(cache=cache)

    ### PUBLIC PROPERTIES ###

    @property
    def material_package_manager_wrangler(self):
        r'''Score manager material package maker wrangler:

        ::

            >>> score_manager.material_package_manager_wrangler
            MaterialPackageManagerWrangler()

        Returns material package maker wrangler.
        '''
        return self._material_package_manager_wrangler

    @property
    def material_package_wrangler(self):
        r'''Score manager material package wrangler:

        ::

            >>> score_manager.material_package_wrangler
            MaterialPackageWrangler()

        Returns material package wrangler.
        '''
        return self._material_package_wrangler

    @property
    def score_package_wrangler(self):
        r'''Score manager score package wrangler:

        ::

            >>> score_manager.score_package_wrangler
            ScorePackageWrangler()

        Returns score package wrangler.
        '''
        return self._score_package_wrangler

    @property
    def segment_package_wrangler(self):
        r'''Score manager segment package wrangler:

        ::

            >>> score_manager.segment_package_wrangler
            SegmentPackageWrangler()

        Returns segment package wrangler.
        '''
        return self._segment_package_wrangler

    @property
    def stylesheet_file_wrangler(self):
        r'''Score manager stylesheet file wrangler:

        ::

            >>> score_manager.stylesheet_file_wrangler
            StylesheetFileWrangler()

        Returns stylesheet file wrangler.
        '''
        return self._stylesheet_file_wrangler

    ### PUBLIC METHODS ###

    def display_active_scores(self):
        self.session.display_active_scores()

    def display_all_scores(self):
        self.session.display_all_scores()

    def display_mothballed_scores(self):
        self.session.display_mothballed_scores()

    def fix_visible_scores(self):
        self.score_package_wrangler.fix_visible_assets()

    def interactively_edit_score(self, score_package_path):
        manager = self.score_package_wrangler._initialize_asset_manager(
            score_package_path)
        score_package_name = score_package_path.split('.')[-1]
        manager.session.snake_case_current_score_name = score_package_name
        manager._run(cache=True)
        self.session.snake_case_current_score_name = None

    def interactively_make_new_score(self):
        self.score_package_wrangler.interactively_make_asset(rollback=True)

    def interactively_run_tests_on_all_user_scores(self, prompt=True):
        command = 'pytest {}'.format(
            self.configuration.user_score_packages_directory_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self.session.io_manager.display(
                lines, capitalize_first_character=False)
        line = 'tests complete.'
        self.session.io_manager.proceed(line, is_interactive=prompt)

    def manage_materials(self):
        self.material_package_wrangler._run(
            rollback=True, 
            head=self.configuration.built_in_material_packages_package_path,
            )

    def manage_repository(self, clear=True):
        while True:
            self.session.push_breadcrumb('repository commands')
            menu = self._make_repository_menu()
            result = menu._run(clear=clear)
            if self.session.is_backtracking_to_score:
                self.session.is_backtracking_to_score = False
                self.session.pop_breadcrumb()
                continue
            elif self.session.backtrack():
                break
            self._handle_repository_menu_result(result)
            if self.session.backtrack():
                break
            self.session.pop_breadcrumb()
        self.session.pop_breadcrumb()

    def manage_stylesheets(self):
        self.stylesheet_file_wrangler._run(
            rollback=True, 
            )

    def profile_visible_scores(self):
        self.score_package_wrangler.profile_visible_assets()

    def write_cache(self):
        cache_file_path = os.path.join(
                self.configuration.configuration_directory_path, 'cache.py')
        cache_file_pointer = file(cache_file_path, 'w')
        cache_file_pointer.write('start_menu_entries = [\n')
        menu_entries = self.score_package_wrangler._make_asset_menu_entries()
        for menu_entry in menu_entries:
            cache_file_pointer.write('{},\n'.format(menu_entry))
        cache_file_pointer.write(']\n')
        cache_file_pointer.close()

    ### UI MANIFEST ###

    user_input_to_action = {
        'active':       display_active_scores,
        'all':          display_all_scores,
        'fix':          fix_visible_scores,
        'm':            manage_materials,
        'mothballed':   display_mothballed_scores,
        'new':          interactively_make_new_score,
        'profile':      profile_visible_scores,
        'rep':          manage_repository,
        'test':         interactively_run_tests_on_all_user_scores,
        'y':            manage_stylesheets,
        'wc':           write_cache,
        }
