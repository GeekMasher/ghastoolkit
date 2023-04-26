import os
from ghastoolkit.codeql.databases import CodeQLDatabaseList

path = os.path.expanduser("~/.codeql/databases/")
print(f"Loading Path :: {path}")

databases = CodeQLDatabaseList.findDatabases(path)

for database in databases:
    print(f"{database}")

