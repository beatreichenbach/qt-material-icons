import logging

from qt_material_icons import extract

OUTPUT_DIR = '../mypackage'


def test_extract_package() -> None:
    extract.extract_package(output=OUTPUT_DIR)


def extract_icons_multi() -> None:
    names = ('blur_off', 'blur_on', 'deblur', 'tune')
    extract.extract_icons_multi(names=names, output=OUTPUT_DIR)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, force=True)
    test_extract_package()
    extract_icons_multi()
