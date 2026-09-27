from pathlib import Path

import pytest

from qt_material_icons import MaterialIcon, extract


def test_extract_icon(tmp_path: Path) -> None:
    MaterialIcon.import_resource(MaterialIcon.Style.OUTLINED, 20)
    path = extract.extract_icon(
        name='home',
        style=MaterialIcon.Style.OUTLINED,
        fill=False,
        size=20,
        output=str(tmp_path),
    )
    assert path == (
        'material-design-icons/symbols/web/home/materialsymbolsoutlined/home_20px.svg'
    )
    assert (tmp_path / path).exists()


def test_extract_icon_missing(tmp_path: Path) -> None:
    MaterialIcon.import_resource(MaterialIcon.Style.OUTLINED, 20)
    with pytest.raises(OSError):
        extract.extract_icon(
            name='not_an_icon',
            style=MaterialIcon.Style.OUTLINED,
            fill=False,
            size=20,
            output=str(tmp_path),
        )


def test_extract_package(tmp_path: Path) -> None:
    extract.extract_package(output=str(tmp_path))
    package = tmp_path / 'qt_material_icons'
    assert (package / '__init__.py').exists()
    assert (package / '_icon.py').exists()


def test_extract_icons(tmp_path: Path) -> None:
    extract.extract_icons(
        output=str(tmp_path),
        names=['home'],
        style=MaterialIcon.Style.OUTLINED,
        size=20,
    )
    resource = tmp_path / 'qt_material_icons' / 'resources' / 'icons_outlined_20.py'
    assert resource.exists()
    assert resource.stat().st_size


def test_extract_icons_missing(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match='no icons extracted'):
        extract.extract_icons(output=str(tmp_path), names=['not_an_icon'])


def test_extract_icons_multi(tmp_path: Path) -> None:
    extract.extract_icons_multi(
        names=['home'],
        styles=[MaterialIcon.Style.OUTLINED],
        sizes=[20, 24],
        output=str(tmp_path),
    )
    resources = tmp_path / 'qt_material_icons' / 'resources'
    assert (resources / 'icons_outlined_20.py').exists()
    assert (resources / 'icons_outlined_24.py').exists()
