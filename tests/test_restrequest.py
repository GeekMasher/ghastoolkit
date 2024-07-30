"""Test RestRequest class."""

import unittest
from ghastoolkit.errors import GHASToolkitError
import responses

from ghastoolkit.octokit.octokit import RestRequest
from ghastoolkit.octokit.github import GitHub


class TestRestRequest(unittest.TestCase):
    def setUp(self) -> None:
        GitHub.init(repository="GeekMasher/ghastoolkit@main")

        self.rest = RestRequest()

        return super().setUp()

    @responses.activate
    def test_errors(self):
        responses.add(
            responses.GET,
            "https://api.github.com/repos/GeekMasher/ghastoolkit/secret-scanning/alerts",
            json={
                "message": "Secret scanning is disabled on this repository.",
                "documentation_url": "https://docs.github.com/rest/secret-scanning/secret-scanning",
            },
            status=404,
        )
        responses.add(
            responses.GET,
            "https://api.github.com/repos/GeekMasher/ghastoolkit/secret-scanning/alerts/1",
            json={
                "message": "Not Found",
                "documentation_url": "https://docs.github.com/rest/secret-scanning/secret-scanning",
            },
            status=404,
        )

        with self.assertRaises(GHASToolkitError):
            self.rest.get("/repos/{owner}/{repo}/secret-scanning/alerts")

        with self.assertRaises(GHASToolkitError):
            self.rest.get("/repos/{owner}/{repo}/secret-scanning/alerts/1")

    @responses.activate
    def test_error_handler(self):
        responses.add(
            responses.GET,
            "https://api.github.com/repos/GeekMasher/ghastoolkit/secret-scanning/alerts",
            json={
                "message": "Secret scanning is disabled on this repository.",
                "documentation_url": "https://docs.github.com/rest/secret-scanning/secret-scanning",
            },
            status=404,
        )

        def handle(code, _):
            self.assertEqual(code, 404)

        self.rest.get(
            "/repos/{owner}/{repo}/secret-scanning/alerts", error_handler=handle
        )
