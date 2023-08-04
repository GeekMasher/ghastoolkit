# Supply Chain CLI

```bash
python -m ghastoolkit.supplychain --help
```

## Organization Audit

The CLI mode allows you to audit an entire organization to see if:

1. If a repository has an unwanted license
2. If a repository has an unknown license by GitHub

To use this, we need to enable the `org-audit` mode in the supplychain cli:

```bash
python -m ghastoolkit.supplychain org-audit \
  -r "org/repo"
```

The only required argument is the `-r/--repository` which sets the owner and
repository for `ghastoolkit`.

You can also update the licenses you want to check for using `--licenses`,
using `,` as a separater, and widecards to help with versions of licenses.

```bash
python -m ghastoolkit.supplychain org-audit \
  -r "org/repo" \
  --licenses "MIT*,Apache*"
```

Finally you can also set the `--debug` flag to see the different repositories
being analysed:

```bash
python -m ghastoolkit.supplychain org-audit \
  -r "org/repo" \
  --debug
```
