import unittest
import responses

from ghastoolkit import GHASToolkitError, CodeScanning, GitHub
from ghastoolkit.octokit.codescanning import (
    CodeScanningAnalysis,
    CodeScanningAnalysisEnvironment,
    CodeScanningTool,
)

from ghastoolkit.octokit.codescanning import CodeScanning
from ghastoolkit.octokit.github import GitHub
from ghastoolkit.octokit.repository import Repository


class TestCodeScanning(unittest.TestCase):
    def setUp(self) -> None:
        GitHub.init("GeekMasher/ghastoolkit")
        return super().setUp()

    def test_codescanning_default(self):
        cs = CodeScanning()
        self.assertEqual(cs.repository.display(), "GeekMasher/ghastoolkit")

        cs = CodeScanning(GitHub.repository)
        self.assertEqual(cs.repository.display(), "GeekMasher/ghastoolkit")

        GitHub.init("Sample/Repo")
        cs = CodeScanning(GitHub.repository)
        self.assertEqual(cs.repository.display(), "Sample/Repo")

    @responses.activate
    def test_default(self):
        repo = Repository("GeekMasher", "ghastoolkit", reference="refs/heads/main")

        responses.add(
            responses.GET,
            "https://api.github.com/repos/GeekMasher/ghastoolkit/code-scanning/analyses",
            content_type="application/json",
            json=[
                {
                    "ref": "refs/head/main",
                    "commit_sha": "abcdef",
                    "analysis_key": "dynamic/github-code-scanning/codeql:analyze",
                    "environment": '{"language":"python"}',
                    "category": "/language:python",
                    "error": "",
                    "created_at": "2024-08-27T10:35:05Z",
                    "results_count": 0,
                    "rules_count": 50,
                    "id": 1234,
                    "url": "https://api.github.com/repos/...",
                    "sarif_id": "absdef",
                    "tool": {"name": "CodeQL", "guid": None, "version": "2.18.2"},
                    "deletable": True,
                    "warning": "",
                }
            ],
            status=200,
        )

        codescanning = CodeScanning(repo)
        analyses = codescanning.getAnalyses(GitHub.repository.reference)

        self.assertEqual(len(analyses), 1)

        analysis = analyses[0]
        self.assertEqual(type(analysis), CodeScanningAnalysis)
        self.assertEqual(analysis.ref, "refs/head/main")

    @responses.activate
    def test_errors(self):
        repo = Repository("GeekMasher", "ghastoolkit", reference="refs/pull/1/head")
        responses.add(
            responses.GET,
            "https://api.github.com/repos/GeekMasher/ghastoolkit/code-scanning/analyses",
            json={
                "message": "Resource not found",
                "documentation_url": "https://docs.github.com/rest/code-scanning/code-scanning",
            },
            status=404,
        )

        codescanning = CodeScanning(repo)

        with self.assertRaises(GHASToolkitError):
            codescanning.getAnalyses(repo.reference)

    @responses.activate
    def test_retries(self):
        # Reference is a Default Setup for a Pull Request
        repo = Repository("GeekMasher", "ghastoolkit", reference="refs/pull/1/head")
        self.assertTrue(repo.isInPullRequest())

        # First try isn't avalible
        responses.add(
            responses.GET,
            "https://api.github.com/repos/GeekMasher/ghastoolkit/code-scanning/analyses",
            content_type="application/json",
            json=[],
            status=200,
        )
        # Second try its avalible
        responses.add(
            responses.GET,
            "https://api.github.com/repos/GeekMasher/ghastoolkit/code-scanning/analyses",
            content_type="application/json",
            json=[
                {
                    "ref": "refs/pull/1/head",
                    "commit_sha": "abcdef",
                    "analysis_key": "dynamic/github-code-scanning/codeql:analyze",
                    "environment": '{"language":"python"}',
                    "category": "/language:python",
                    "error": "",
                    "created_at": "2024-08-27T10:35:05Z",
                    "results_count": 0,
                    "rules_count": 0,
                    "id": 1234,
                    "url": "https://api.github.com/repos/...",
                    "sarif_id": "absdef",
                    "tool": {"name": "CodeQL", "guid": None, "version": "2.18.2"},
                    "deletable": True,
                    "warning": "",
                }
            ],
            status=200,
        )

        # Enable retries
        codescanning = CodeScanning(repo, retry_count=5, retry_sleep=0)
        self.assertEqual(codescanning.retry_count, 5)
        self.assertEqual(codescanning.retry_sleep, 0)

        analyses = codescanning.getAnalyses(repo.reference)

        self.assertEqual(len(analyses), 1)
        analysis = analyses[0]
        self.assertEqual(type(analysis), CodeScanningAnalysis)
        self.assertEqual(analysis.ref, "refs/pull/1/head")

        # Test the dicts are all loaded correctly
        self.assertEqual(type(analysis.tool), CodeScanningTool)
        self.assertEqual(analysis.tool.name, "CodeQL")

        self.assertEqual(type(analysis.environment), CodeScanningAnalysisEnvironment)
        self.assertEqual(analysis.environment.language, "python")
