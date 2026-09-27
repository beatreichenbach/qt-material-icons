import logging
import os
import subprocess

from qt_material_icons import MaterialIcon
from qt_material_icons.create import create_resource_file, qrc_file, write_qrc_file

BUILD_DIR = 'build'
SIZES = (20, 24, 40, 48)
REPOSITORY_URL = 'https://github.com/google/material-design-icons'


def clone_repo() -> None:
    """Clone the source repo."""

    repo = 'material-design-icons'

    if not os.path.exists(repo):
        logging.info(f'Cloning repo: {REPOSITORY_URL}')

        subprocess.run(
            ['git', 'clone', '--filter=blob:none', '--sparse', REPOSITORY_URL, repo],
            check=True,
        )
        subprocess.run(
            ['git', 'sparse-checkout', 'set', 'symbols/web'],
            cwd=repo,
            check=True,
        )

    logging.info(f'Pulling repo: {repo}')
    subprocess.run(['git', 'pull', 'origin', 'master'], cwd=repo, check=True)


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
