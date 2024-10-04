import os.path
import sys

from PySide6 import QtWidgets, QtCore

from qt_material_icons import MaterialIcon


def main(screen_grab: bool = False) -> None:
    app = QtWidgets.QApplication(sys.argv)

    widget = QtWidgets.QWidget()
    layout = QtWidgets.QGridLayout()
    widget.setLayout(layout)

    size = 48
    icon_size = QtCore.QSize(size, size)
    icon_names = ('folder', 'cancel', 'search', 'home', 'menu', 'settings')
    for i, style in enumerate(MaterialIcon.Style):
        layout.addWidget(QtWidgets.QLabel(f'{style.value}'), i, 0)
        for j, name in enumerate(icon_names):
            icon = MaterialIcon(name, style, size=size)
            button = QtWidgets.QPushButton()
            button.setIcon(icon)
            button.setIconSize(icon_size)
            layout.addWidget(button, i, j + 1)

        for j, name in enumerate(icon_names):
            icon = MaterialIcon(name, style, fill=True, size=size)
            button = QtWidgets.QPushButton()
            button.setIcon(icon)
            button.setIconSize(icon_size)
            layout.addWidget(button, i, len(icon_names) + j + 1)

    widget.show()

    if screen_grab:
        path = os.path.join('..', '.github', 'assets', 'icons.png')
        pixmap = widget.grab()
        pixmap.save(path)

    sys.exit(app.exec())


if __name__ == '__main__':
    main(screen_grab=False)
