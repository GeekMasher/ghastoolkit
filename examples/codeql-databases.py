import os
from ghastoolkit.codeql.databases import CodeQLDatabase, CodeQLDatabases
from ghastoolkit.octokit.github import GitHub, Repository

GitHub.init("GeekMasher/ghastoolkit")

path = os.path.expanduser("~/.codeql/databases/")
os.makedirs(path, exist_ok=True) # create if not present

codeqldb = CodeQLDatabase("ghastoolkit", "python", GitHub.repository)
print(f"- {codeqldb} (existis: {codeqldb.exists()})")
print(f"    [{codeqldb.path}]")

if not codeqldb.exists():
    codeqldb.downloadDatabase(codeqldb.path)


# Load All Local Databases
local_databases = CodeQLDatabases()
local_databases.findDatabases(path)

print("\nAll Local Databases:")
for database in local_databases:
    print(f"  - {database}")


# Load Remote Database
remote_databases = CodeQLDatabases.loadRemoteDatabases(GitHub.repository)
# remote_databases.downloadDatabases()

print("\nAll Remote Databases:")
for database in remote_databases:
    print(f"  - {database}")

