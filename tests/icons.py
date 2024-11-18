import qt_themes
from PySide6 import QtWidgets, QtCore

from qt_material_icons import MaterialIcon
from tests import application


class IconGallery(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget | None = None) -> None:
        super().__init__(parent)

        self._init_ui()

    def _init_ui(self) -> None:
        self.setWindowTitle('Material Icons')
        self.resize(840, 320)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        # Controls
        control_layout = QtWidgets.QHBoxLayout()
        layout.addLayout(control_layout)

        self.style_combo_box = QtWidgets.QComboBox()
        for style in MaterialIcon.Style:
            self.style_combo_box.addItem(style.name.title(), style)
        self.style_combo_box.currentIndexChanged.connect(lambda: self._update_icons())
        control_layout.addWidget(self.style_combo_box)

        self.filled_checkbox = QtWidgets.QPushButton('Filled')
        self.filled_checkbox.setCheckable(True)
        self.filled_checkbox.toggled.connect(lambda: self._update_icons())
        control_layout.addWidget(self.filled_checkbox)

        self.enabled_checkbox = QtWidgets.QPushButton('Enabled')
        self.enabled_checkbox.setCheckable(True)
        self.enabled_checkbox.setChecked(True)
        self.enabled_checkbox.toggled.connect(lambda: self._update_icons())
        control_layout.addWidget(self.enabled_checkbox)

        control_layout.addStretch()

        screenshot_button = QtWidgets.QPushButton('Screenshot')
        screenshot_button.clicked.connect(self._screenshot)
        control_layout.addWidget(screenshot_button)

        # Icons
        self.icon_layout = QtWidgets.QGridLayout()
        self.icon_widget = QtWidgets.QWidget()
        self.icon_widget.setLayout(self.icon_layout)
        layout.addWidget(self.icon_widget)
        layout.setStretch(1, 1)

        self._update_icons()

    def _update_icons(self) -> None:
        self.icon_widget.deleteLater()

        self.icon_widget = QtWidgets.QWidget()
        self.layout().addWidget(self.icon_widget)
        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(64, 64, 64, 64)
        self.icon_widget.setLayout(layout)

        size = 24
        icon_size = QtCore.QSize(48, 48)
        style = self.style_combo_box.currentData()
        fill = self.filled_checkbox.isChecked()

        # Icons
        group_box = QtWidgets.QGroupBox()
        layout.addWidget(group_box)
        icon_layout = QtWidgets.QGridLayout()
        group_box.setLayout(icon_layout)

        names = (
            'arrow_back',
            '3d_rotation',
            'call_split',
            'edit',
            'home',
            'favorite',
            'alarm_add',
            'apps',
            'mic',
            'insert_chart',
            'shopping_cart',
            'settings',
            'mail',
            'headphones',
            'check_circle',
            'today',
            'search',
            'download',
        )
        columns = 6
        for i, name in enumerate(names):
            column = i % columns
            row = i // columns

            icon = MaterialIcon(name, style=style, size=size, fill=fill)
            button = QtWidgets.QPushButton()
            button.setIcon(icon)
            button.setIconSize(icon_size)
            button.setFlat(True)
            button.setEnabled(self.enabled_checkbox.isChecked())
            icon_layout.addWidget(button, row, column)

        # Colors
        group_box = QtWidgets.QGroupBox()
        layout.addWidget(group_box)
        color_layout = QtWidgets.QGridLayout()
        group_box.setLayout(color_layout)

        theme = qt_themes.get_theme()

        icons = []
        icon = MaterialIcon('info', style=style, size=size, fill=fill)
        icon.set_color(theme.blue)
        icons.append(icon)
        icon = MaterialIcon('folder', style=style, size=size, fill=fill)
        icon.set_color(theme.cyan)
        icons.append(icon)
        icon = MaterialIcon('check_circle', style=style, size=size, fill=fill)
        icon.set_color(theme.green)
        icons.append(icon)
        icon = MaterialIcon('warning', style=style, size=size, fill=fill)
        icon.set_color(theme.orange)
        icons.append(icon)
        icon = MaterialIcon('error', style=style, size=size, fill=fill)
        icon.set_color(theme.red)
        icons.append(icon)
        icon = MaterialIcon('report', style=style, size=size, fill=fill)
        icon.set_color(theme.magenta)
        icons.append(icon)

        columns = 2
        for i, icon in enumerate(icons):
            column = i % columns
            row = i // columns

            button = QtWidgets.QPushButton()
            button.setIcon(icon)
            button.setIconSize(icon_size)
            button.setFlat(True)
            button.setEnabled(self.enabled_checkbox.isChecked())
            color_layout.addWidget(button, row, column)

        layout.setStretch(0, 3)
        layout.setStretch(1, 1)

    def _screenshot(self) -> None:
        path = '../.github/assets/icons.png'
        pixmap = self.icon_widget.grab()
        pixmap.save(path)


def test_icons() -> None:
    with application():
        widget = IconGallery()
        widget.show()


if __name__ == '__main__':
    test_icons()
