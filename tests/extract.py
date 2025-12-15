import logging

from qt_material_icons import extract

OUTPUT_DIR = '../mypackage'


def extract_icons_multi() -> None:
    extract.extract_icons_multi(
        names=('home', 'computer'),
        output=OUTPUT_DIR,
    )


def test_extract_package() -> None:
    extract.extract_package(output=OUTPUT_DIR)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, force=True)
    test_extract_package()
    extract_icons_multi()
