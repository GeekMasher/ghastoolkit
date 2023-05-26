import logging
from ghastoolkit.codeql.databases import CodeQLDatabase, CodeQLDatabases
from ghastoolkit.octokit.codescanning import CodeScanning
from ghastoolkit.octokit.dependencygraph import DependencyGraph
from ghastoolkit.octokit.github import GitHub


def header(name: str):
    print("#" * 32)
    print(f"    {name}")
    print("#" * 32)
    print("")


def codeqlDatabaseList(arguments):
    dbs = CodeQLDatabases.loadLocalDatabase()
    for database in dbs:
        print(f"- {database}")


def codeqlDatabaseDownload(arguments):
    dbs = CodeScanning(GitHub.repository).getCodeQLDatabases()
    if len(dbs) == 0:
        logging.error(f"CodeQL Database wasn't found on GitHub")
        logging.error(
            f"Please make sure you have access to where the database is stord"
        )
        exit(1)
    for db in dbs:
        db = CodeQLDatabase(
            GitHub.repository.repo, db.get("language", ""), repository=GitHub.repository
        )
        if db.exists():
            logging.info("CodeQL Databases are already present")
            continue
        # TODO this needs fixed
        db.downloadDatabase(db.createDownloadPath())


def codeScanningAlerts(arguments):
    header("Code Scanning")
    codescanning = CodeScanning(GitHub.repository)
    alerts = codescanning.getAlerts()

    print(f"Total Alerts :: {len(alerts)}")

    analyses = codescanning.getLatestAnalyses(GitHub.repository.reference)
    print(f"\nTools:   ({len(analyses)})")

    for analyse in analyses:
        tool = analyse.get("tool", {}).get("name")
        version = analyse.get("tool", {}).get("version")
        created_at = analyse.get("created_at")

        print(f" - {tool} v{version} ({created_at})")


def depGraph(arguments):
    header("Dependency Graph")

    depgraph = DependencyGraph(GitHub.repository)
    bom = depgraph.exportBOM()
    packages = bom.get("sbom", {}).get("packages", [])

    print(f"Total Dependencies :: {len(packages)}")

    info = bom.get("sbom", {}).get("creationInfo", {})
    print(f"Created :: {info.get('created')}")

    print("\nTools:")
    for tool in info.get("creators", []):
        print(f" - {tool}")
