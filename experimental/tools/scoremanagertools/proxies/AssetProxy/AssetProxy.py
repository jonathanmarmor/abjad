import abc
import os
import shutil
import subprocess
from experimental.tools.scoremanagertools.core.ScoreManagerObject import ScoreManagerObject
from experimental.tools.scoremanagertools.menuing.UserInputGetter import UserInputGetter


class AssetProxy(ScoreManagerObject):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta
    generic_class_name = 'asset'

    ### INITIALIZER ###

    def __init__(self, path=None, session=None):
        assert isinstance(path, (str, type(None)))
        ScoreManagerObject.__init__(self, session=session)
        self._path = path

    ### SPECIAL METHODS ###

    def __repr__(self):
        if self.path:
            return '{}({!r})'.format(self._class_name, self.path)
        else:
            return '{}()'.format(self._class_name)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def breadcrumb(self):
        return self.short_name or self._human_readable_class_name

    @property
    def exists(self):
        if self.path:
            return os.path.exists(self.path)
        return False

    @property
    def human_readable_name(self):
        return self.short_name

    @property
    def is_versioned(self):
        if self.path is None:
            return False
        if not os.path.exists(self.path):
            return False
        command = 'svn st {}'.format(self.path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        first_line = proc.stdout.readline()
        if first_line.startswith(('?', 'svn: warning:')):
            return False
        else:
            return True

    @property
    def parent_directory_name(self):
        if self.path:
            return os.path.dirname(self.path)

    @property
    def path(self):
        return self._path

    @property
    def plural_generic_class_name(self):
        return self.pluralize_string(self.generic_class_name)

    @property
    def short_name(self):
        if self.path:
            return self.path.split(os.path.sep)[-1]

    @property
    def short_name_without_extension(self):
        if self.short_name:
            if '.' in self.short_name:
                return self.short_name[:self.short_name.rindex('.')]
            else:
                return self.short_name

    @property
    def svn_add_command(self):
        if self.path:
            return 'svn add {}'.format(self.path)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def conditionally_make_empty_asset(self, is_interactive=False):
        pass

    def copy(self, new_path):
        shutil.copyfile(self.path, new_path)

    def copy_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        getter = self.make_getter()
        getter.append_underscore_delimited_lowercase_file_name('new name')
        result = getter.run()
        if self.backtrack():
            return
        new_asset_short_name = self.human_readable_name_to_asset_short_name(result)
        new_path = os.path.join(self.parent_directory_name, new_asset_short_name)
        self.display('new path will be {}'.format(new_path))
        if not self.confirm():
            return
        self.copy(new_path)
        self.proceed('asset copied.')

    @abc.abstractmethod
    def fix(self):
        pass

    def human_readable_name_to_asset_short_name(self, human_readable_name):
        asset_short_name = human_readable_name.lower()
        asset_short_name = asset_short_name.replace(' ', '_')
        return asset_short_name

    @abc.abstractmethod
    def profile(self):
        pass

    def remove(self):
        if self.is_versioned:
            return self.remove_versioned_asset()
        else:
            return self.remove_nonversioned_asset()

    def remove_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.display(['{} will be removed.'.format(self.path), ''])
        getter = self.make_getter(where=self.where())
        getter.append_string("type 'remove' to proceed")
        result = getter.run()
        if self.backtrack():
            return
        if not result == 'remove':
            return
        if self.remove():
            self.proceed('{} removed.'.format(self.path))

    def remove_nonversioned_asset(self):
        command = 'rm -rf {}'.format(self.path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        proc.stdout.readline()
        return True

    def remove_versioned_asset(self, is_interactive=False):
        command = 'svn --force rm {}'.format(self.path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc.stdout.readline()
        return True

    def rename(self, new_path):
        if self.is_versioned:
            result = self.rename_versioned_asset(new_path)
        else:
            result = self.rename_nonversioned_asset(new_path)

    def rename_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        getter = self.make_getter(where=self.where())
        getter.append_underscore_delimited_lowercase_file_name('new human-readable name')
        getter.include_newlines = False
        result = getter.run()
        if self.backtrack():
            return
        new_path = os.path.join(self.parent_directory_name, result)
        self.display(['new path name will be: "{}"'.format(new_path), ''])
        if not self.confirm():
            return
        if self.rename(new_path):
            self.proceed('asset renamed.')

    def rename_nonversioned_asset(self, new_path):
        command = 'mv {} {}'.format(self.path, new_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc.stdout.readline()
        self._path = new_path

    def rename_versioned_asset(self, new_path):
        command = 'svn --force mv {} {}'.format(self.path, new_path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        proc.stdout.readline()
        self._path = new_path

    def run(self, cache=False, clear=True, user_input=None):
        self.assign_user_input(user_input=user_input)
        self.cache_breadcrumbs(cache=cache)
        while True:
            self.push_breadcrumb()
            menu = self.make_main_menu()
            result = menu.run(clear=clear)
            if self.backtrack(source=self.backtracking_source):
                break
            elif not result:
                self.pop_breadcrumb()
                continue
            self.handle_main_menu_result(result)
            if self.backtrack(source=self.backtracking_source):
                break
            self.pop_breadcrumb()
        self.pop_breadcrumb()
        self.restore_breadcrumbs(cache=cache)

    def run_first_time(self, **kwargs):
        self.run(**kwargs)

    def run_py_test(self, prompt=True):
        proc = subprocess.Popen('py.test {}'.format(self.path), shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        if lines:
            self.display(lines)
        line = 'tests run.'
        self.proceed(line, is_interactive=prompt)

    def svn_add(self, is_interactive=False):
        if is_interactive:
            self.display(self.path)
        proc = subprocess.Popen(self.svn_add_command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        if is_interactive:
            self.display(lines)
        self.proceed(is_interactive=is_interactive)

    def svn_ci(self, commit_message=None, is_interactive=True):
        if commit_message is None:
            getter = self.make_getter(where=self.where())
            getter.append_string('commit message')
            commit_message = getter.run()
            if self.backtrack():
                return
            line = 'commit message will be: "{}"\n'.format(commit_message)
            self.display(line)
            if not self.confirm():
                return
        lines = []
        lines.append(self.path)
        command = 'svn commit -m "{}" {}'.format(commit_message, self.path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines.extend([line.strip() for line in proc.stdout.readlines()])
        lines.append('')
        self.display(lines)
        self.proceed(is_interactive=is_interactive)

    def svn_st(self, is_interactive=True):
        if is_interactive:
            self.display(self.path)
        command = 'svn st -u {}'.format(self.path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.display(lines)
        self.proceed(is_interactive=is_interactive)

    def svn_up(self, is_interactive=True):
        if is_interactive:
            self.display(self.path)
        command = 'svn up {}'.format(self.path)
        proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
        lines = [line.strip() for line in proc.stdout.readlines()]
        lines.append('')
        self.display(lines)
        self.proceed(is_interactive=is_interactive)

    def touch(self):
        os.system('touch {}'.format(self.path))

    def write_boilerplate_asset_to_disk(self, boilerplate_asset_name):
        if not os.path.exists(boilerplate_asset_name):
            boilerplate_asset_name = os.path.join(
                self.configuration.boilerplate_directory_name, boilerplate_asset_name)
        if os.path.exists(boilerplate_asset_name):
            shutil.copyfile(boilerplate_asset_name, self.path)
            return True

    def write_boilerplate_asset_to_disk_interactively(self, user_input=None):
        self.assign_user_input(user_input=user_input)
        getter = self.make_getter(where=self.where())
        getter.append_underscore_delimited_lowercase_file_name('name of boilerplate asset')
        self.push_backtrack()
        boilerplate_asset_name = getter.run()
        self.pop_backtrack()
        if self.backtrack():
            return
        if self.write_boilerplate_asset_to_disk(boilerplate_asset_name):
            self.proceed('boilerplate asset copied.')
        else:
            self.proceed('boilerplate asset {!r} does not exist.'.format(boilerplate_asset_name))