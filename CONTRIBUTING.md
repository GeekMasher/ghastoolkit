# Contributing to GHASToolkit

The GHASToolkit project is an open-source library and CLI for working with the different features of GitHub Advance Security. We welcome contributions from the community! Here are some guidelines to help you get started.

## Issues

The easiest way to contribute is to report issues. If you find a bug or have a feature request, please open an issue on the [GitHub repository](https://github.com/geekmasher/ghastoolkit/issues).

## Requirements

- `python` 3.10 or higher
- [`uv`](https://github.com/astral-sh/uv)

GHASToolkit needs to be able to run on all supported versions of Python. Please make sure to test your changes on all supported versions.

## Building

To build the project, you just need to run the following command:

```bash
uv build
```

If you are having issues building / running the project, you might need to set the `PYTHONPATH` environment variable to the root of the project. You can do this by running the following command:

```bash
export PYTHONPATH=$PWD/src
```

### Code Formatting

GHASToolkit uses `black` for code formatting. To format the code, you can use the following command:

```bash
uv run black .
```

## Testing

GHASToolkit uses `unittest` for testing. To run the tests, you can use the following command:

```bash
uv run python -m unittest discover -v -s ./tests -p 'test_*.py'
```

## Running CLI

To run the CLI, you can use the following command:

```bash
uv run python -m ghastoolkit --help
```

## Documentation

GHASToolkit uses `sphinx` for documentation. To build the documentation, run the following command:

```bash
uv run sphinx-build -b html ./docs ./public
```

*Note:* This might change in the future, but for now, the documentation is built using `sphinx` and hosted on GitHub Pages. You can find the documentation at [https://ghastoolkit.github.io/](https://ghastoolkit.github.io/).
