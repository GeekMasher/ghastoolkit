
import unittest

from ghastoolkit.octokit.github import GitHub
from ghastoolkit.octokit.secretscanning import SecretScanning

class TestSecretScanning(unittest.TestCase):
    def setUp(self) -> None:
        GitHub.init("GeekMasher/ghastoolkit")
        return super().setUp()

    def test_secretscanning_default(self):
        return


    def test_codescanning_default(self):
        ss = SecretScanning()
        self.assertEqual(ss.repository.display(), "GeekMasher/ghastoolkit")    
        
        ss = SecretScanning(GitHub.repository)
        self.assertEqual(ss.repository.display(), "GeekMasher/ghastoolkit")    

        GitHub.init("Sample/Repo")
        ss = SecretScanning(GitHub.repository)
        self.assertEqual(ss.repository.display(), "Sample/Repo")
