import logging
import os
import subprocess

from qt_material_icons import MaterialIcon

SIZES = (20, 24, 40, 48)


def clone_repo() -> None:
    repo = 'material-design-icons'

    if not os.path.exists(repo):
        url = 'https://github.com/google/material-design-icons'
        logging.info(f'Cloning repo: {url}')

        os.makedirs(repo)
        subprocess.run('git init', cwd=repo, shell=True)
        subprocess.run(
            f'git remote add -f origin {url}',
            cwd=repo,
            shell=True,
        )
        subprocess.run('git config core.sparseCheckout true', cwd=repo, shell=True)
        with open(os.path.join(repo, '.git', 'info', 'sparse-checkout'), 'a') as f:
            f.write('symbols/web/')

    # logging.info(f'Pulling repo: {repo}')
    # subprocess.run(
    #     'git pull origin master',
    #     cwd=repo,
    #     shell=True,
    # )


def collect_files(force: bool = False) -> None:
    for style in MaterialIcon.Style:
        for size in SIZES:
            qrc_path = get_qrc_path(style, size)
            if not force and os.path.exists(qrc_path):
                logging.debug(f'Path already exists, skipping: {qrc_path}')
                continue
            if not os.path.exists(os.path.dirname(qrc_path)):
                os.makedirs(os.path.dirname(qrc_path))
            logging.info(f'Collecting files for: {qrc_path}')

            files = []
            root = os.path.join('material-design-icons', 'symbols', 'web')
            for icon in os.listdir(root):
                style_path = os.path.join(
                    '..', root, icon, f'materialsymbols{style.value}'
                )
                files.append(os.path.join(style_path, f'{icon}_{size}px.svg'))
                files.append(os.path.join(style_path, f'{icon}_fill1_{size}px.svg'))

            with open(qrc_path, 'w') as f:
                f.write('<!DOCTYPE RCC>\n<RCC version="1.0">\n')
                f.write('<qresource>\n')
                for file in files:
                    path = file.replace('\\', '/')
                    f.write(f'<file>{path}</file>\n')
                f.write('</qresource>\n')
                f.write('</RCC>\n')


def build_resource() -> None:
    for style in MaterialIcon.Style:
        for size in SIZES:
            qrc_path = get_qrc_path(style, size)
            logging.info(f'Building resource for: {qrc_path}')

            resource_path = os.path.join(
                'qt_material_icons', 'resources', f'icons_{style.value}_{size}.py'
            )
            result = subprocess.run(['pyside6-rcc', qrc_path, '-o', resource_path])
            result.check_returncode()
            patch_backwards_compatibility(resource_path)


def patch_backwards_compatibility(path: str) -> None:
    logging.info(f'Patching backwards compatibility for: {path}')

    with open(path, 'r') as f:
        content = f.read()

    old = 'from PySide6 import QtCore'
    new = (
        'try:\n'
        '    from PySide6 import QtCore\n'
        'except ImportError:\n'
        '    from PySide2 import QtCore'
    )
    content = content.replace(old, new)

    with open(path, 'w') as f:
        f.write(content)


def get_qrc_path(style: MaterialIcon.Style, size: int) -> str:
    return os.path.join('build', f'material_design_icons_{style.value}_{size}.qrc')


def main() -> None:
    logging.basicConfig(level=logging.INFO, force=True)
    clone_repo()
    collect_files()
    build_resource()


if __name__ == '__main__':
    main()
