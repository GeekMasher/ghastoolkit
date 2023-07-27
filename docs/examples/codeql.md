# CodeQL

## CLI

To use the CodeQL CLI in Python, you need to first import `CodeQL` and set it up:

```python
from ghastoolkit import CodeQL, CodeQLDatabases

codeql = CodeQL()
databases = CodeQLDatabases.loadLocalDatabase()   # ~/.codeql/databases
# or can load and download remote databases

print(f"CodeQL    :: {codeql}")
print(f"Databases :: {len(databases)}")
```

## Running Queries

By default you can run the default queries on a database which will run the
standard CodeQL query pack `codeql/$LANGUAGE-queries`.

```python
# get a single database by name
db = databases.get("ghastoolkit")

results = codeql.runQuery(db)
print(f"Results   :: {len(results)}")
```

If you want to run a suites from the default packs on the database, use one of
the built-in suites:

```python
# security-extended
results = codeql.runQuery(db, "security-extended")

# security-and-quality
results = codeql.runQuery(db, "security-and-quality")

# security-experimental
results = codeql.runQuery(db, "security-experimental")
```

You can also output the command to the console using `display` versus it being
hidden by default.

```python
codeql.runQuery(db, display=True)
```

## Custom Packs

To run a query from a custom pack, you can use the following pattern.

```python
from ghastoolkit import CodeQL, CodeQLDatabases, CodeQLPack

codeql = CodeQL()
databases = CodeQLDatabases.loadLocalDatabase()

# download the latest pack
pack = CodeQLPack.download("geekmasher/codeql-python")
print(f"Pack: {pack} (queries: {len(pack.resolveQueries())})")

for db in databases:
    results = codeql.runQuery(db, pack.name)
    print(f" >> {db} :: {len(results)}")
```
