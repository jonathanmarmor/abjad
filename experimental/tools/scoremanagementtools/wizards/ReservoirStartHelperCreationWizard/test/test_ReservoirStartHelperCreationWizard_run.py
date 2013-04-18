from experimental import *


def test_ReservoirStartHelperCreationWizard_run_01():

    wizard = scoremanagementtools.wizards.ReservoirStartHelperCreationWizard()
    assert wizard.run(user_input='q') == []

    wizard = scoremanagementtools.wizards.ReservoirStartHelperCreationWizard()
    assert wizard.run(user_input='b') == []


def test_ReservoirStartHelperCreationWizard_run_02():

    wizard = scoremanagementtools.wizards.ReservoirStartHelperCreationWizard()
    assert wizard.run(user_input='start~at~index~0') == [('start at index 0', ())]