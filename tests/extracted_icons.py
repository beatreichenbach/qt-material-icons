from PySide6 import QtWidgets

from mypackage.qt_material_icons import MaterialIcon
from tests import application


def test_icons() -> None:
    with application():
        widget = QtWidgets.QWidget()
        widget.resize(480, 320)
        layout = QtWidgets.QHBoxLayout()
        widget.setLayout(layout)

        names = ('blur_off', 'blur_on', 'deblur', 'tune')
        for name in names:
            icon = MaterialIcon(name=name, fill=True)
            button = QtWidgets.QPushButton()
            button.setIcon(icon)
            button.setFlat(True)
            layout.addWidget(button)
        widget.show()


if __name__ == '__main__':
    test_icons()
