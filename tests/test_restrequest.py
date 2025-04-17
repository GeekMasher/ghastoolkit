"""Test RestRequest class."""

import unittest
import utils
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
        utils.loadResponses("restrequests.json", "errors")

        with self.assertRaises(GHASToolkitError):
            self.rest.get("/repos/{owner}/{repo}/secret-scanning/alerts")

        with self.assertRaises(GHASToolkitError):
            self.rest.get("/repos/{owner}/{repo}/secret-scanning/alerts/1")

    @responses.activate
    def test_error_handler(self):
        utils.loadResponses("restrequests.json", "error_handler") 

        def handle(code, _):
            self.assertEqual(code, 404)

        self.rest.get(
            "/repos/{owner}/{repo}/secret-scanning/alerts", error_handler=handle
        )
