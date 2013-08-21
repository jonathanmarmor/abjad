from abjad import *


def test_ComponentInspector_get_annotation_value_01():

    staff = Staff("c'8 d'8 e'8 f'8")
    annotation = marktools.Annotation('special dictionary', {})
    annotation.attach(staff[0])

    assert inspect(staff[0]).get_annotation_value('special dictionary') == {}