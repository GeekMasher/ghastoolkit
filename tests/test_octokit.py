from dataclasses import dataclass, is_dataclass
import unittest

from ghastoolkit.octokit.octokit import OctoItem, Octokit, loadOctoItem
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


@dataclass
class Example(OctoItem):
    number: int


class TestLoadOctoItem(unittest.TestCase):
    def test_load(self):
        item = loadOctoItem(Example, {"number": 5})

        self.assertTrue(isinstance(item, Example))
        self.assertTrue(is_dataclass(item))

        self.assertEqual(item.number, 5)
