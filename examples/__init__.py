import contextlib
import sys
from collections.abc import Iterator

import qt_themes
from PySide6 import QtWidgets


@contextlib.contextmanager
def application() -> Iterator[QtWidgets.QApplication]:
    """Run the Qt event loop with the example theme."""

    theme = 'one_dark_two'
    app = QtWidgets.QApplication.instance()
    if isinstance(app, QtWidgets.QApplication):
        qt_themes.set_theme(theme)
        yield app
        return

    app = QtWidgets.QApplication(sys.argv)
    qt_themes.set_theme(theme)
    yield app
    app.exec()
