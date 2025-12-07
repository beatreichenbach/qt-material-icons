import logging
import os
import subprocess

from qt_material_icons import MaterialIcon
from qt_material_icons.create import create_resource_file, qrc_file, write_qrc_file

BUILD_DIR = 'build'
SIZES = (20, 24, 40, 48)


def clone_repo() -> None:
    """Clone the source repo."""

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


def create_qrc_files(force: bool = False) -> None:
    """Create the resource files for all icon sets."""

    for style in MaterialIcon.Style:
        for size in SIZES:
            qrc_path = os.path.join(BUILD_DIR, qrc_file(style, size))

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

            write_qrc_file(qrc_path, files)


def create_resource_files() -> None:
    """Create resource files for all styles and sizes."""

    for style in MaterialIcon.Style:
        for size in SIZES:
            qrc_path = os.path.join(BUILD_DIR, qrc_file(style, size))
            resource_path = os.path.join(
                'qt_material_icons', 'resources', f'icons_{style.value}_{size}.py'
            )
            create_resource_file(qrc_path=qrc_path, resource_path=resource_path)


def main() -> None:
    logging.basicConfig(level=logging.INFO, force=True)
    clone_repo()
    create_qrc_files()
    create_resource_files()


if __name__ == '__main__':
    main()
