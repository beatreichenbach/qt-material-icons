from PySide6 import QtCore, QtGui, QtWidgets

from qt_material_icons import MaterialIcon
from qt_material_icons._icon import fill_pixmap


def test_style_values() -> None:
    assert MaterialIcon.Style('outlined') is MaterialIcon.Style.OUTLINED
    assert MaterialIcon.Style('rounded') is MaterialIcon.Style.ROUNDED
    assert MaterialIcon.Style('sharp') is MaterialIcon.Style.SHARP


def test_resource_path() -> None:
    path = MaterialIcon.resource_path('home', MaterialIcon.Style.ROUNDED, False, 24)
    assert path == (
        ':/material-design-icons/symbols/web/home/materialsymbolsrounded/home_24px.svg'
    )


def test_resource_path_fill() -> None:
    path = MaterialIcon.resource_path('home', MaterialIcon.Style.ROUNDED, True, 24)
    assert path.endswith('home_fill1_24px.svg')


def test_resource_exists(qapp: QtWidgets.QApplication) -> None:
    MaterialIcon.import_resource(MaterialIcon.Style.OUTLINED, 20)
    assert MaterialIcon.resource_exists('home', MaterialIcon.Style.OUTLINED, False, 20)
    assert MaterialIcon.resource_exists('home', MaterialIcon.Style.OUTLINED, True, 20)
    assert not MaterialIcon.resource_exists(
        'not_an_icon', MaterialIcon.Style.OUTLINED, False, 20
    )


def test_material_icon(qapp: QtWidgets.QApplication) -> None:
    icon = MaterialIcon('home', style=MaterialIcon.Style.ROUNDED, size=24)
    assert icon.name == 'home'
    assert repr(icon) == "MaterialIcon('home')"
    pixmap = icon.pixmap(24)
    assert not pixmap.isNull()
    assert pixmap.size() == QtCore.QSize(24, 24)


def test_pixmap_default_size(qapp: QtWidgets.QApplication) -> None:
    icon = MaterialIcon('home', size=24)
    assert icon.pixmap().size() == QtCore.QSize(24, 24)


def test_pixmap_color(qapp: QtWidgets.QApplication) -> None:
    icon = MaterialIcon('home', size=24)
    pixmap = icon.pixmap(24, color=QtGui.QColor('red'))
    assert not pixmap.isNull()


def test_fill_pixmap(qapp: QtWidgets.QApplication) -> None:
    pixmap = QtGui.QPixmap(4, 4)
    pixmap.fill(QtGui.QColor('white'))
    filled = fill_pixmap(pixmap, QtGui.QColor('red'))
    assert filled.toImage().pixelColor(0, 0) == QtGui.QColor('red')
    assert pixmap.toImage().pixelColor(0, 0) == QtGui.QColor('white')


def test_set_color(qapp: QtWidgets.QApplication) -> None:
    icon = MaterialIcon('home', size=24)
    icon.set_color(QtGui.QColor('red'))
    icon.set_color(QtGui.QColor('red'), mode=QtGui.QIcon.Mode.Disabled)


def test_set_icon(qapp: QtWidgets.QApplication) -> None:
    icon = MaterialIcon('home', size=24)
    other = MaterialIcon('search', size=24)
    icon.set_icon(other, state=QtGui.QIcon.State.On)
    icon.set_icon(QtGui.QIcon(other.pixmap(24)))
