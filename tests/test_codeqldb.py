import os
import unittest

from ghastoolkit.codeql.databases import CodeQLDatabase, Repository


class TestCodeQLDb(unittest.TestCase):
    def setUp(self):
        self.repo = Repository("GeekMasher", "ghastoolkit")

    def test_path(self):
        codeql = CodeQLDatabase("db", "java", self.repo)
        self.assertEqual(
            codeql.createDownloadPath("/tmp"),
            os.path.join("/tmp", "java", "GeekMasher", "ghastoolkit"),
        )

        codeql = CodeQLDatabase("db", "java")
        self.assertEqual(
            codeql.createDownloadPath("/tmp"), os.path.join("/tmp", "java", "db")
        )
    
    def test_pack(self):
        codeql = CodeQLDatabase("db", "java", self.repo)
        self.assertEqual(codeql.default_pack, "codeql/java-queries")

    def test_suite(self):
        codeql = CodeQLDatabase("db", "java", self.repo)
        self.assertEqual(codeql.getSuite("code-scanning"), "codeql/java-queries:codeql-suites/java-code-scanning.qls")


