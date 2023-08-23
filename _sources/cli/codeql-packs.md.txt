# CodeQL Packs

## Subcommands

### Version Bumping

To update your packs version number, you can use the `version` subcommand.

```bash
python -m ghastoolkit.codeql.packs version --help
```

You can also set the type of bumping using the `--bump [type]` command.

```bash
python -m ghastoolkit.codeql.packs version --bump patch
```

This will result in the CodeQL Pack being version bumped correctly based on the type.

## Features

### Updating Dependencies

To update your packs dependencies to the latest version, you can use the `--latest`
argument.

```bash
python -m ghastoolkit.codeql.packs --latest
```

Updating dependencies can work along with `version` subcommand to both update and
bump your packs version.
