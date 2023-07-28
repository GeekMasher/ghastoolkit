"""CodeQL Example."""
import os
from ghastoolkit import CodeQL, CodeQLDatabase
from ghastoolkit.octokit.github import GitHub

GitHub.init(os.environ.get("GITHUB_REPOSITORY", "GeekMasher/ghastoolkit"))

codeql = CodeQL()
print(codeql)


db = CodeQLDatabase("ghastoolkit", "python", GitHub.repository)
codeql.createDatabase(db, display=True)

print("")
if not db:
    print("Failed to load Database...")
    exit(1)

print(f"Database :: {db} ({db.path})")
if not db.exists():
    print("Downloading database...")
    db.downloadDatabase()

results = codeql.runQuery(db, "security-extended", display=True)

print(f"\nResults: {len(results)}\n")

for result in results:
    print(f"- {result}")
