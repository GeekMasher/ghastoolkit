
import unittest

from ghastoolkit.supplychain.dependencies import Dependencies, Dependency
from ghastoolkit.supplychain.licensing import Licenses


class TestLicensing(unittest.TestCase):
    def setUp(self) -> None:
        self.licenses = Licenses()
        self.licenses.add("pkg:maven/com.geekmasher/ghastoolkit", ["MIT"])

        return super().setUp()

    def test_find(self):
        result = self.licenses.find("pkg:maven/com.geekmasher/ghastoolkit")
        self.assertEqual(result, ["MIT"])

    def test_apply(self):
        dependencies = Dependencies()
        dependencies.append(Dependency("ghastoolkit", "com.geekmasher", manager="maven"))
        self.assertEqual(len(dependencies), 1)
        
        dependencies.applyLicenses(self.licenses)

        dep = dependencies.pop(0)
        self.assertTrue(isinstance(dep, Dependency))
        self.assertEqual(dep.licence, "MIT")


