from __future__ import annotations

import enum
import importlib

try:
    from PySide6 import QtWidges, QtGui
except ImportError:
    from PySide2 import QtWidgets, QtGui


class MaterialIcon(QtGui.QIcon):
    class Style(enum.Enum):
        OUTLINED = 'outlined'
        ROUNDED = 'rounded'
        SHARP = 'sharp'

    OUTLINED = Style.OUTLINED
    ROUNDED = Style.ROUNDED
    SHARP = Style.SHARP

    def __init__(
        self, name: str, style: Style = Style.OUTLINED, fill: bool = False
    ) -> None:
        super().__init__()

        import_resource(style)

        self.name = name
        file_name = f'{name}_fill1_24px.svg' if fill else f'{name}_24px.svg'
        self._path = (
            f':/material-design-icons/symbols/web/{name}/'
            f'materialsymbols{style.value}/{file_name}'
        )
        self._pixmap = QtGui.QPixmap(self._path)

        self._init_colors()

    def __repr__(self) -> str:
        return f'{self.__class__.__name__}({self.name!r})'

    def _init_colors(self) -> None:
        palette = QtWidgets.QApplication.palette()
        role = QtGui.QPalette.ColorRole.WindowText
        self._color_normal = palette.color(QtGui.QPalette.ColorGroup.Normal, role)
        self._color_disabled = palette.color(QtGui.QPalette.ColorGroup.Disabled, role)
        state = QtGui.QIcon.State.Off
        self.set_color(self._color_normal, QtGui.QIcon.Mode.Normal, state)
        self.set_color(self._color_disabled, QtGui.QIcon.Mode.Disabled, state)

    def set_icon(
        self,
        icon: QtGui.QIcon,
        mode: QtGui.QIcon.Mode = QtGui.QIcon.Mode.Normal,
        state: QtGui.QIcon.State = QtGui.QIcon.State.Off,
    ):
        if isinstance(icon, MaterialIcon):
            pixmap = icon._pixmap
        else:
            pixmap = icon.pixmap(self._pixmap.size())
        self.addPixmap(pixmap, mode, state)

    def pixmap(
        self,
        extent: int = 0,
        mode: QtGui.QIcon.Mode = QtGui.QIcon.Mode.Normal,
        state: QtGui.QIcon.State = QtGui.QIcon.State.Off,
        color: QtGui.QColor | None = None,
    ) -> QtGui.QPixmap:
        if extent:
            # HACK: QPixmap causes crashes in PySide2.
            # pixmap = QtGui.QPixmap(self._path).scaledToWidth(extent)
            pixmap = QtGui.QIcon(self._path).pixmap(extent)
        else:
            pixmap = self._pixmap

        if color is None:
            if state == QtGui.QIcon.State.Off and mode == QtGui.QIcon.Mode.Disabled:
                color = self._color_disabled
            else:
                color = self._color_normal
        return fill_pixmap(pixmap, color)

    def set_color(
        self,
        color: QtGui.QColor,
        mode: QtGui.QIcon.Mode = QtGui.QIcon.Mode.Normal,
        state: QtGui.QIcon.State = QtGui.QIcon.State.Off,
    ):
        pixmap = fill_pixmap(self._pixmap, color)
        self.addPixmap(pixmap, mode, state)


def import_resource(style: MaterialIcon.Style) -> None:
    """
    Imports the resource for Qt, separated by style to not load unneeded SVGs.
    """
    importlib.import_module(f'.icons_{style.value}', package=f'{__package__}.resources')


def fill_pixmap(pixmap: QtGui.QPixmap, color: QtGui.QColor) -> QtGui.QPixmap:
    """
    Return a copy of 'pixmap' filled with 'color'.
    """
    pixmap = QtGui.QPixmap(pixmap)
    painter = QtGui.QPainter(pixmap)
    painter.setCompositionMode(QtGui.QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(pixmap.rect(), color)
    painter.end()
    return pixmap


__all__ = ['MaterialIcon']
