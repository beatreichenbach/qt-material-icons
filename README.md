# qt-material-icons

[![PyPI version](https://img.shields.io/pypi/v/qt-material-icons.svg)](https://pypi.org/project/qt-material-icons/)
[![Python](https://img.shields.io/badge/python-3.6%2B-blue.svg)](https://pypi.org/project/qt-material-icons/)
[![License](https://img.shields.io/pypi/l/qt-material-icons.svg)](https://github.com/beatreichenbach/qt-material-icons/blob/main/LICENSE)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![ty](https://img.shields.io/badge/type%20checked-ty-261230.svg)](https://github.com/astral-sh/ty)

A Python library that enables [Material Symbols / Material Icons](https://github.com/google/material-design-icons)
by Google to be used in Qt using PySide.

![Header](https://raw.githubusercontent.com/beatreichenbach/qt-material-icons/refs/heads/main/.github/assets/header.png)

## Installation

Install using pip:
```shell
pip install qt-material-icons
```

The available Qt extras are `pyside6`, `pyside2`, and `qtpy`.

## Usage

```python
from PySide6 import QtGui
from qt_material_icons import MaterialIcon

# Create a QIcon object
icon = MaterialIcon('search')

# Set a color
color = QtGui.QColor('red')
icon.set_color(color)

# Set a color for a state, for example when a button is checked
icon.set_color(color, state=QtGui.QIcon.State.On)

# Set a different icon for a state, for example when a button is checked
toggle_icon = MaterialIcon('toggle_off')
toggle_icon_on = MaterialIcon('toggle_on')
toggle_icon.set_icon(toggle_icon_on, state=QtGui.QIcon.State.On)
```

Refer to [Google Material Symbols & Icons] for browsing icons.

[Google Material Symbols & Icons]: https://fonts.google.com/icons

### Localize qt-material-icons

Since the `qt-material-icons` package is quite large with all the resource files, a cli is provided to extract 
specific icons so they can be shipped alongside the package.

> [!WARNING]
The `qtmaterialicons` cli requires Python 3.9 or later.

Install as a dev dependency:
```toml
# pyproject.toml
[project.optional-dependencies]
dev = ["qt-material-icons"]
```

Use the cli to extract icons:
```shell
qtmaterialicons -o mypackage --styles outlined rounded --sizes 20 24 --names home computer search favorite
```

Then import in your repo:
```python
from mypackage.qt_material_icons import MaterialIcon
```

## Contributing

To contribute please refer to the [Contributing Guide](CONTRIBUTING.md).

## License

MIT License. Copyright 2024 - Beat Reichenbach. See the [License file](LICENSE) for details.

The [Material Symbols / Material Icons](https://github.com/google/material-design-icons) are licensed under
[Apache License Version 2.0](https://github.com/google/material-design-icons/blob/master/LICENSE).
