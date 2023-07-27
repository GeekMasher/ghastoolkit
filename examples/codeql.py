"""CodeQL Example."""
import os
from ghastoolkit import CodeQL, CodeQLDatabases
from ghastoolkit.octokit.github import GitHub

GitHub.init(os.environ.get("GITHUB_REPOSITORY", "GeekMasher/ghastoolkit"))

codeql = CodeQL()
print(codeql)

# load remote databases
dbs = CodeQLDatabases.loadRemoteDatabases(GitHub.repository)
print(f"Remote Databases :: {len(dbs)}")
for db in dbs:
    print(f" >> {db}")

print("")
db = dbs.get("ghastoolkit")

if not db:
    print("Failed to load Database...")
    exit(1)

print(f"Database :: {db}")
if not db.exists():
    print("Downloading database...")
    db.downloadDatabase()

results = codeql.runQuery(db, "codeql/python-queries", display=True)

print(f"\nResults: {len(results)}\n")

for result in results:
    print(f"- {result}")
