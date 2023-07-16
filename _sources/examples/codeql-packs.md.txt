# CodeQL Pack

First lets import and download the `codeql/python-queries` pack with the version
set to `0.8.0`. This will automatically download the pack for us.

```python
from ghastoolkit import CodeQLPack, CodeQLPacks

pack = CodeQLPack.download("codeql/python-queries", "0.8.0")
print(f"Pack :: {pack}")
```

Otherwise you can load via a path

```python
pack = CodeQLPack("~/.codeql/packages/codeql/python-queries/0.8.0")
print(f"Pack :: {pack}")
```

Or load a collection of packs using the `CodeQLPacks` API.

```python
packs = CodeQLPacks("~/.codeql/packages")
print(f"Packs :: {len(packs)}")
for pack in packs:
    print(f" -> {pack}")
```

## Custom Packs

If you are creating custom packs and want to do all the things, you can use the
easy to use APIs to make your life easier.

### Install Pack Dependencies

To resolve and install the pack dependencies, you can use the following:

```python
pack.install()
```

### Create Pack and Install it locally

To create a pack and install it locally on the current system:

```python
path = pack.create()
print(f"Pack Install Path :: {path}")
```

### Resolve Pack Queries

To get a list of all the queries in the pack you can use the `resolveQueries()` API.

```python
queries = pack.resolveQueries()
print(f"# Queries :: {len(queries)}")
for query in queries:
    print(f" - {query}")
```
