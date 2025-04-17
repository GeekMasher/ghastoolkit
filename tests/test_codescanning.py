import unittest
import responses
import utils

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
        utils.loadResponses("codescanning.json", "default")

        repo = Repository("GeekMasher", "ghastoolkit", reference="refs/heads/main")

        codescanning = CodeScanning(repo)
        analyses = codescanning.getAnalyses(GitHub.repository.reference)

        self.assertEqual(len(analyses), 1)

        analysis = analyses[0]
        self.assertEqual(type(analysis), CodeScanningAnalysis)
        self.assertEqual(analysis.ref, "refs/head/main")

    @responses.activate
    def test_errors(self):
        utils.loadResponses("codescanning.json", "errors")

        repo = Repository("GeekMasher", "ghastoolkit", reference="refs/pull/1/head")

        codescanning = CodeScanning(repo)

        with self.assertRaises(GHASToolkitError):
            codescanning.getAnalyses(repo.reference)

    @responses.activate
    def test_retries(self):
        utils.loadResponses("codescanning.json", "retries")

        # Reference is a Default Setup for a Pull Request
        repo = Repository("GeekMasher", "ghastoolkit", reference="refs/pull/1/head")
        self.assertTrue(repo.isInPullRequest())

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
