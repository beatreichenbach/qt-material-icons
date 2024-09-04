# qt-material-icons

A Python library that enables [Material Symbols / Material Icons] by Google
to be used in Qt using PySide.

## Installation

Install using pip:
```shell
pip install qt-material-icons
```

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


![Screenshot of the icons](/.github/assets/icons.png)

Refer to [Google Material Symbols & Icons] for browsing icons.

[Google Material Symbols & Icons]: https://fonts.google.com/icons

## Contributing

To contribute please refer to the [Contributing Guide](CONTRIBUTING.md).

## License

MIT License. Copyright 2024 - Beat Reichenbach.
See the [License file](LICENSE) for details.

The [Material Symbols / Material Icons] are licensed under
[Apache License Version 2.0](https://github.com/google/material-design-icons/blob/master/LICENSE).

[Material Symbols / Material Icons]: https://github.com/google/material-design-icons