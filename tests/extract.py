import logging

from qt_material_icons import MaterialIcon, extract

OUTPUT_DIR = '../mypackage'


def test_extract_icons() -> None:
    extract.extract_icons(
        names=('home', 'computer'),
        styles=(MaterialIcon.Style.OUTLINED,),
        fill=True,
        output=OUTPUT_DIR,
    )


def test_extract_package() -> None:
    extract.extract_package(output=OUTPUT_DIR)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, force=True)
    test_extract_package()
    test_extract_icons()
