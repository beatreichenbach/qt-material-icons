# Contributing Guide

## Development

To get started:

```sh
uv venv --python 3.13
uv pip install -e ".[dev]"
pre-commit install
```

To update Material Symbols resources:

```shell
python compile_icons.py
```

Run the checks:

```shell
ruff format qt_material_icons examples tests
ruff check --select I --fix qt_material_icons examples tests
ruff check qt_material_icons examples tests
ty check
pytest
```

### Releasing Changes

To version up using [python-semantic-release](https://github.com/python-semantic-release/python-semantic-release):

```shell
semantic-release version
```
