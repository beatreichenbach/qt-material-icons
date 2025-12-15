import argparse
import logging

from qt_material_icons import MaterialIcon, extract


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Extracts a qt_material_icons resources.'
    )

    parser.add_argument(
        '--names',
        type=str,
        nargs='+',
        help='The icon names (e.g., home, account_circle).',
    )

    parser.add_argument(
        '--styles',
        type=str,
        nargs='+',
        default=('outlined',),
        choices=['outlined', 'rounded', 'sharp'],
        help='The icon styles (outlined, rounded, sharp).',
    )
    parser.add_argument(
        '--sizes',
        type=int,
        nargs='+',
        default=(20,),
        choices=[20, 24, 40, 48],
        help='The icon size (20, 24, 40, 48).',
    )
    parser.add_argument(
        '-o',
        '--output',
        type=str,
        required=True,
        help=(
            'The path to save the final compiled Python resource file '
            '(e.g., mypackage).'
        ),
    )

    args = parser.parse_args()

    styles = tuple(MaterialIcon.Style(s) for s in args.styles)

    extract.extract_package(output=args.output)
    extract.extract_icons_multi(
        names=args.names,
        styles=styles,
        sizes=args.sizes,
        output=args.output,
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    main()
