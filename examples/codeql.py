"""CodeQL Example."""
import os
from ghastoolkit import CodeQL, CodeQLDatabases
from ghastoolkit.octokit.github import GitHub

GitHub.init(os.environ.get("GITHUB_REPOSITORY", "GeekMasher/ghastoolkit"))

codeql = CodeQL()
print(codeql)

# load local databases
dbs = CodeQLDatabases.loadRemoteDatabases(GitHub.repository)
print(f"Remote Databases :: {len(dbs)}")

db = dbs[0]
if not db:
    print("Failed to load Database...")
    exit(1)

print(f"Database :: {db}")
db.downloadDatabase()

results = codeql.runQuery(db)

print(f"\nResults: {len(results)}\n")

for result in results:
    print(f"- {result}")
