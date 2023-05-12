from datetime import datetime
import os
import tempfile
import unittest

import yaml

from ghastoolkit.codeql.databases import CodeQLDatabase, Repository


class TestCodeQLDb(unittest.TestCase):
    def setUp(self):
        self.repo = Repository("GeekMasher", "ghastoolkit")

        self.codeql_path_yml = os.path.join(tempfile.gettempdir(), "codeql.yml")

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

    def test_yml_loading(self):
        data = {
            "sourceLocationPrefix": "/tmp/ghastoolkit",
            "baselineLinesOfCode": 42069,
            "primaryLanguage": "python",
            "creationMetadata": {
                "creationTime": "2023-01-01T16:20:00.000000000Z"
            }
        }
        with open(self.codeql_path_yml, 'w') as handle:
            yaml.safe_dump(data, handle)

        self.assertTrue(os.path.exists(self.codeql_path_yml))

        db = CodeQLDatabase.loadFromYml(self.codeql_path_yml)
        self.assertEqual(db.name, "ghastoolkit")
        self.assertEqual(db.language, "python")
        self.assertEqual(db.loc_baseline, 42069)

        time = datetime.fromisoformat("2023-01-01T16:20:00")
        self.assertEqual(db.created, time)

