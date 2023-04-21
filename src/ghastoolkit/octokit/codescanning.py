import logging
from typing import Any, Optional
from ghastoolkit.octokit.github import Repository
from ghastoolkit.octokit.octokit import RestRequest

logger = logging.getLogger("ghastoolkit.octokit.codescanning")


class CodeScanning:
    def __init__(self, repository: Repository) -> None:
        self.rest = RestRequest(repository)

    def getOrgAlerts(self, state: str = "open") -> list[dict[Any, Any]]:
        results = self.rest.get(
            "/orgs/{org}/code-scanning/alerts", {"state": state}, authenticated=True
        )
        return results

    def getAlerts(
        self, state: str = "open", tool_name: Optional[str] = None
    ) -> list[dict]:
        """Get a code scanning alert

        https://docs.github.com/en/rest/code-scanning?apiVersion=2022-11-28#get-a-code-scanning-alert
        """
        results = self.rest.get(
            "/repos/{owner}/{repo}/code-scanning/alerts",
            {"state": state, "tool_name": tool_name},
            authenticated=True,
        )
        return results

    def getAlert(self, alert_number: int) -> dict:
        results = self.rest.get(
            "/repos/{owner}/{repo}/code-scanning/alerts/{alert_number}",
            {"alert_number": alert_number},
            authenticated=True,
        )
        return results

    # CodeQL

    def getCodeQLDatabases(self) -> list[dict]:
        """List CodeQL databases for a repository

        https://docs.github.com/en/rest/code-scanning?apiVersion=2022-11-28#list-codeql-databases-for-a-repository
        """
        return self.rest.get("/repos/{owner}/{repo}/code-scanning/codeql/databases")

    def getCodeQLDatabase(self, language: str) -> dict:
        """Get a CodeQL database for a repository
        https://docs.github.com/en/rest/code-scanning?apiVersion=2022-11-28#get-a-codeql-database-for-a-repository
        """
        return self.rest.get(
            "/repos/{owner}/{repo}/code-scanning/codeql/databases/{language}",
            {"language": language},
        )
