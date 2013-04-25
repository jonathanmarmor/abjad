from experimental.tools.scoremanagertools.proxies.AssetProxy import AssetProxy
import os
import subprocess


class DirectoryProxy(AssetProxy):

    ### SPECIAL METHODS ###

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.path == other.path:
                return True
        return False

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.path)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def directory_contents(self):
        result = []
        for file_name in os.listdir(self.path):
            if file_name.endswith('.pyc'):
                path = os.path.join(self.path, file_name)
                os.remove(path)
        for name in os.listdir(self.path):
            if not name.startswith('.'):
                result.append(name)
        return result

    @property
    def directory_name(self):
        return self._path

    @property
    def public_content_paths(self):
        result = []
        for short_name in os.listdir(self.path):
            if short_name[0].isalpha():
                if not short_name.endswith('.pyc'):
                    result.append(os.path.join(self.path, short_name))
        return result

    @property
    def public_content_short_names(self):
        result = []
        for short_name in os.listdir(self.path):
            if short_name[0].isalpha():
                if not short_name.endswith('.pyc'):
                    result.append(short_name)
        return result

    @property
    def svn_add_command(self):
        return 'cd {} && svn-add-all'.format(self.path)

    ### PUBLIC METHODS ###

    def conditionally_make_empty_asset(self, is_interactive=False):
        self.print_not_yet_implemented()

    def fix(self, is_interactive=False):
        pass

    def get_directory_name_interactively(self):
        getter = self.make_getter(where=self.where())
        getter.append_string('directory name')
        result = getter.run()
        if self.backtrack():
            return
        self.path = result

    def make_directory(self):
        os.mkdir(self.path)

    def print_directory_contents(self):
        self.display(self.directory_contents, capitalize_first_character=False)
        self.display('')
        self.session.hide_next_redraw = True

    def profile(self):
        pass