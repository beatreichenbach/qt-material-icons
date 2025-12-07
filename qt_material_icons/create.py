import logging
import re
import subprocess
from collections.abc import Sequence

from qt_material_icons import MaterialIcon

logger = logging.getLogger(__name__)


def write_qrc_file(path: str, files: Sequence[str]) -> None:
    """Write the files to a qrc xml file."""

    with open(path, 'w') as f:
        f.write('<!DOCTYPE RCC>\n<RCC version="1.0">\n')
        f.write('<qresource>\n')
        for file in files:
            file_path = file.replace('\\', '/')
            f.write(f'<file>{file_path}</file>\n')
        f.write('</qresource>\n')
        f.write('</RCC>\n')


def create_resource_file(qrc_path: str, resource_path: str) -> None:
    """Create resource file from a qrc file."""

    logging.debug(f'Using qrc file: {qrc_path}')
    logging.info(f'Creating resource file: {qrc_path}')

    result = subprocess.run(['pyside6-rcc', qrc_path, '-o', resource_path])
    try:
        result.check_returncode()
    except subprocess.CalledProcessError:
        logger.debug(result.stderr)
        logger.error(result.stderr)
        return
    patch_imports(resource_path)


def patch_imports(path: str) -> None:
    """Patch resource file to work with all Qt imports."""

    logging.info(f'Patching imports for resource file: {path}')

    with open(path, 'r') as f:
        content = f.read()

    old = r'from \w+ import QtCore'
    new = (
        'try:\n'
        '    from qtpy import QtCore, QtGui, QtWidgets\n'
        'except ImportError:\n'
        '    try:\n'
        '        from PySide6 import QtCore, QtGui, QtWidgets\n'
        '    except ImportError:\n'
        '        from PySide2 import QtCore, QtGui, QtWidgets\n'
    )
    content = re.sub(old, new, content, count=1)

    with open(path, 'w') as f:
        f.write(content)


def qrc_file(style: MaterialIcon.Style, size: int) -> str:
    """Return the qrc filename for a style and size."""

    return f'material_design_icons_{style.value}_{size}.qrc'
