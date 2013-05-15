import os
from experimental import *


def test_MusicPackageProxy_01():

    music_proxy = scoremanagertools.proxies.MusicPackageProxy(
        'scoremanagertools.built_in_scores.red_example_score')

    assert music_proxy.filesystem_path == os.path.join(
        music_proxy.configuration.score_manager_tools_directory_path, 
        'built_in_scores', 'red_example_score', 'music')
    assert music_proxy.filesystem_basename == 'music'
    assert music_proxy.package_path == \
        'experimental.tools.scoremanagertools.built_in_scores.red_example_score.music'