import contextlib
import sys

import qt_themes
from PySide6 import QtWidgets


@contextlib.contextmanager
def application() -> QtWidgets.QApplication:
    theme = 'one_dark_two'
    if app := QtWidgets.QApplication.instance():
        qt_themes.set_theme(theme)
        yield app
        return

    app = QtWidgets.QApplication(sys.argv)
    qt_themes.set_theme(theme)
    yield app
    app.exec()
