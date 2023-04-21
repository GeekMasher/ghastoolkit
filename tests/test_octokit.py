import unittest

from ghastoolkit.octokit.octokit import Octokit
from ghastoolkit.octokit.github import GitHub


class TestOctokit(unittest.TestCase):
    def setUp(self) -> None:
        GitHub.init(repository="GeekMasher/ghastoolkit@main")
        return super().setUp()

    def test_route(self):
        route = Octokit.route(
            "/repos/{owner}/{repo}/secret-scanning/alerts", GitHub.repository
        )
        self.assertEqual(
            route,
            "https://api.github.com/repos/GeekMasher/ghastoolkit/secret-scanning/alerts",
        )
