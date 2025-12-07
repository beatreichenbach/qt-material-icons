from PySide6 import QtWidgets

from mypackage.qt_material_icons import MaterialIcon
from tests import application


def test_icons() -> None:
    with application():
        icon = MaterialIcon(name='home', fill=True)
        button = QtWidgets.QPushButton()
        button.setIcon(icon)
        button.setFlat(True)
        button.show()


if __name__ == '__main__':
    test_icons()
