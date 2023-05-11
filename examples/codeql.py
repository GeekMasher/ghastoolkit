
import json
import os
from ghastoolkit.codeql import databases
from ghastoolkit.codeql.cli import CodeQL 
from ghastoolkit.codeql.databases import CodeQLDatabases

codeql = CodeQL()
print(codeql)

dbs = CodeQLDatabases.loadLocalDatabase()
db = dbs.get("python-GeekMasher_ghastoolkit")
print(db)

results = codeql.runQuery(db)

print(f"\nResults: {len(results)}\n")

for result in results:
    print(f"- {result}")


