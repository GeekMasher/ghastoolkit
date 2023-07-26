"""CodeQL Example."""
import os
import json
from ghastoolkit import CodeQL, CodeQLDatabases

codeql = CodeQL()
print(codeql)

dbs = CodeQLDatabases.loadLocalDatabase()
db = dbs.get("python-GeekMasher_ghastoolkit")
print(db)

results = codeql.runQuery(db)

print(f"\nResults: {len(results)}\n")

for result in results:
    print(f"- {result}")
