import importlib.util
import logging
import os
import shutil
import tempfile
from collections.abc import Sequence

try:
    from qtpy import QtCore
except ImportError:
    try:
        from PySide6 import QtCore
    except ImportError:
        from PySide2 import QtCore

from qt_material_icons import MaterialIcon
from qt_material_icons.create import create_resource_file, qrc_file, write_qrc_file

logger = logging.getLogger(__name__)


def extract_icon(
    name: str,
    style: MaterialIcon.Style,
    fill: bool,
    size: int,
    output: str,
) -> str:
    """Extract an icon and return the filename relative to the root."""

    resource_path = MaterialIcon.resource_path(name, style, fill, size)

    qfile = QtCore.QFile(resource_path)
    if not qfile.open(QtCore.QIODevice.OpenModeFlag.ReadOnly):
        logger.error(f'Could not open source resource file: {resource_path}')
        raise OSError

    svg_data = qfile.readAll()
    qfile.close()

    if svg_data.isEmpty():
        logger.error(f'Source resource is empty at {resource_path}')
        raise OSError

    # Match the same directory structure to preserve qrc paths
    icon_path = resource_path[2:]
    output_file = os.path.join(output, icon_path)
    os.makedirs(os.path.dirname(output_file), exist_ok=True)

    with open(output_file, 'wb') as f:
        f.write(svg_data.data())

    return icon_path


def extract_icons(
    output: str,
    names: Sequence[str],
    style: MaterialIcon.Style = MaterialIcon.Style.OUTLINED,
    size: int = 20,
) -> None:
    """
    Extract the icons matching the names for the given style and size and create a
    resource file in the output directory.
    """

    MaterialIcon.import_resource(style, size)

    with tempfile.TemporaryDirectory() as temp_dir:
        filenames = []

        for name in names:
            for fill in (True, False):
                try:
                    filename = extract_icon(
                        name=name,
                        style=style,
                        fill=fill,
                        size=size,
                        output=temp_dir,
                    )
                    filenames.append(filename)
                except IOError as e:
                    logger.error(e)
                    continue

        if not filenames:
            logger.error('No files extracted.')
            return

        qrc_path = os.path.join(temp_dir, qrc_file(style, size))
        write_qrc_file(qrc_path, filenames)

        package_name = __package__
        resource_dir = os.path.join(output, package_name, 'resources')
        resource_path = os.path.join(resource_dir, f'icons_{style.value}_{size}.py')

        os.makedirs(resource_dir, exist_ok=True)

        create_resource_file(qrc_path=qrc_path, resource_path=resource_path)


def extract_icons_multi(
    names: Sequence[str],
    styles: Sequence[MaterialIcon.Style] = (MaterialIcon.Style.OUTLINED,),
    sizes: Sequence[int] = (20,),
    output: str = '.',
) -> None:
    """
    Extract the icons matching the names for all styles and sizes and create
    resource files in the output directory.
    """

    for style in styles:
        for size in sizes:
            extract_icons(output=output, names=names, style=style, size=size)


def extract_package(output: str) -> None:
    """Extract the qt-material-icons package and move it into a directory."""

    package_name = __package__
    files = ['__init__.py', '_icon.py']

    spec = importlib.util.find_spec(package_name)
    if spec is None or spec.origin is None:
        logger.error(f'Could not find installed package: {package_name}.')
        raise RuntimeError

    target_dir = os.path.join(output, package_name)
    os.makedirs(target_dir, exist_ok=True)

    for filename in files:
        source_path = os.path.join(os.path.dirname(spec.origin), filename)
        target_path = os.path.join(target_dir, filename)

        if not os.path.exists(source_path):
            logger.warning(f'File not found in site-packages: {source_path}')
            continue

        shutil.copy2(source_path, target_path)
        logger.debug(f'File copied: {target_path}')
