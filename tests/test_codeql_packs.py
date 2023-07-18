import unittest

from ghastoolkit.codeql.packs.pack import CodeQLPack


class TestCodeQLPacks(unittest.TestCase):
    def setUp(self) -> None:
        self.pack = CodeQLPack(name="geekmasher/test", version="1.0.0")
        return super().setUp()

    def test_loaded(self):
        self.assertEqual(self.pack.name, "geekmasher/test")
        self.assertEqual(self.pack.version, "1.0.0")

    def test_qlpack(self):
        # assume without path is default
        self.assertEqual(self.pack.qlpack, "qlpack.yml")

    def test_update_version_major(self):
        version = self.pack.updateVersion("major")
        self.assertEqual(version, "2.0.0")
        self.assertEqual(self.pack.version, "2.0.0")

    def test_update_version_minor(self):
        version = self.pack.updateVersion("minor")
        self.assertEqual(version, "1.1.0")
        self.assertEqual(self.pack.version, "1.1.0")

    def test_update_version_patch(self):
        version = self.pack.updateVersion("patch")
        self.assertEqual(version, "1.0.1")
        self.assertEqual(self.pack.version, "1.0.1")

    def test_update_pack(self):
        self.pack.path = None
        data = self.pack.updatePack()
        self.assertTrue(isinstance(data, dict))
        self.assertEqual(data.get("name"), "geekmasher/test")
        self.assertEqual(data.get("version"), "1.0.0")
        self.assertFalse(data.get("library"))

        # by default, don't export it
        self.assertIsNone(data.get("dependencies"))
        self.assertIsNone(data.get("defaultSuiteFile"))
