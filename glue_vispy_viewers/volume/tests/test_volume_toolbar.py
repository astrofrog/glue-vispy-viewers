
from distutils.version import LooseVersion

import numpy as np

import glue
from glue.core import DataCollection, Data
from glue.app.qt.application import GlueApplication
from glue.core.component import Component
from glue.core.tests.util import simple_session

from ..volume_viewer import VispyVolumeViewer
from ...extern.vispy.app import MouseEvent

GLUE_LT_08 = LooseVersion(glue.__version__) < LooseVersion('0.8')


def make_test_data():

    data = Data(label="Test Cube Data")

    np.random.seed(12345)

    for letter in 'abc':
        comp = Component(np.random.random((10, 10, 10)))
        data.add_component(comp, letter)

    return data


def test_volumeviewer_toolbar():
    session = simple_session()
    v = VispyVolumeViewer(session)
    data = make_test_data()
    v.add_data(data)
    assert v.toolbar is not None

    toolbar = v.toolbar

    # test rotate tool
    toolbar.actions['Rotate'].toggle()
    assert toolbar.active_tool.tool_id == 'Rotate'
    # TODO: assert a mode here
    toolbar.actions['Rotate'].toggle()
    assert toolbar.active_tool is None

    # test lasso selection tool
    toolbar.actions['Lasso'].toggle()
    assert toolbar.active_tool.tool_id == 'Lasso'
    lasso = toolbar.active_tool
    # event = QTest.mouseMove(viewer._vispy_widget)

    # TODO: add a real mouse move event so content in lasso.move() is called
    lasso.press(MouseEvent('mouse_press'))
    lasso.move(MouseEvent('mouse_move'))
    lasso.release(MouseEvent('mouse_release'))
    assert toolbar.tools['Lasso'] == lasso