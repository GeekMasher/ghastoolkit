import unittest

from ghastoolkit.octokit.codescanning import CodeScanning
from ghastoolkit.octokit.github import GitHub


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
