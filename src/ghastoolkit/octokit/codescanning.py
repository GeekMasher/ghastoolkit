import json
import logging
import os
from typing import Any, Optional, Union
from ghastoolkit.octokit.github import GitHub, Repository
from ghastoolkit.octokit.octokit import RestRequest

logger = logging.getLogger("ghastoolkit.octokit.codescanning")


class CodeScanning:
    def __init__(self, repository: Optional[Repository] = None) -> None:
        """GitHub Code Scanning REST API

        https://docs.github.com/en/rest/code-scanning
        """
        self.repository = repository or GitHub.repository
        if not self.repository:
            raise Exception("CodeScanning requires Repository to be set")
        self.rest = RestRequest(self.repository)

    def getOrganizationAlerts(self, state: str = "open") -> list[dict[Any, Any]]:
        """Get Organization Alerts

        https://docs.github.com/en/rest/code-scanning#list-code-scanning-alerts-for-an-organization
        """
        results = self.rest.get(
            "/orgs/{org}/code-scanning/alerts", {"state": state}, authenticated=True
        )
        if isinstance(results, list):
            return results
        raise Exception(f"Error getting alerts from Organization")

    def getAlerts(
        self, state: str = "open", tool_name: Optional[str] = None
    ) -> list[dict]:
        """Get a code scanning alert

        https://docs.github.com/en/rest/code-scanning#list-code-scanning-alerts-for-a-repository
        """
        results = self.rest.get(
            "/repos/{owner}/{repo}/code-scanning/alerts",
            {"state": state, "tool_name": tool_name},
            authenticated=True,
        )
        if isinstance(results, list):
            return results
        raise Exception(f"Error getting list of alerts")

    def getAlert(self, alert_number: int) -> dict:
        """Get Single Alert

        https://docs.github.com/en/rest/code-scanning#get-a-code-scanning-alert
        """
        results = self.rest.get(
            "/repos/{owner}/{repo}/code-scanning/alerts/{alert_number}",
            {"alert_number": alert_number},
            authenticated=True,
        )
        if isinstance(results, dict):
            return results
        raise Exception(f"Error getting alert: {alert_number}")

    def getAnalyses(
        self, reference: Optional[str] = None, tool: Optional[str] = None
    ) -> list[dict]:
        """Get a list of analyses for a repository
        https://docs.github.com/en/enterprise-cloud@latest/rest/code-scanning#list-code-scanning-analyses-for-a-repository
        """
        results = self.rest.get(
            "/repos/{org}/{repo}/code-scanning/analyses",
            {"tool_name": tool, "ref": reference or self.repository.reference},
        )
        if isinstance(results, list):
            return results
        raise Exception(f"")

    def getLatestAnalyses(
        self, reference: Optional[str] = None, tool: Optional[str] = None
    ) -> list[dict]:
        """Get Latest Analyses for every tool"""
        tools = set()
        results = []
        for analysis in self.getAnalyses(reference, tool):
            name = analysis.get("tool", {}).get("name")
            if name in tools:
                continue
            tools.add(name)
            results.append(analysis)

        return results

    def getSarifId(self, url: str) -> int:
        """Get the latest SARIF ID from a URL"""
        if url and "/" in url:
            return int(url.split("/")[-1])
        return -1

    def downloadSARIF(self, output: str, sarif_id: int) -> bool:
        """Get SARIF by ID (UUID)"""
        logger.debug(f"Downloading SARIF file :: {sarif_id}")

        # need to change "Accept" and then reset
        og_accept = self.rest.session.headers.pop("Accept")
        self.rest.session.headers["Accept"] = "application/sarif+json"
        result = self.rest.get(
            "/repos/{org}/{repo}/code-scanning/analyses/{sarif_id}",
            {"sarif_id": sarif_id},
        )
        self.rest.session.headers["Accept"] = og_accept

        logger.debug(f"Saving SARIF file to :: {output}")
        with open(output, "w") as handle:
            json.dump(result, handle, indent=2)
        logger.debug("Saved SARIF file")
        return True

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
