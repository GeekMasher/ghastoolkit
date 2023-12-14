import unittest

from ghastoolkit import *


class TestDefault(unittest.TestCase):
    def test_supplychain(self):
        gp = DependencyGraph()
        deps = Dependencies()
        dep = Dependency("ghastoolkit")

        alert = DependencyAlert(
            0,
            "open",
            "high",
            advisory=Advisory("0000", "high"),
            purl="pypi/ghastoolkit",
        )

        advisory = Advisory("ghas-0000-0000", "high")

    def test_codescanning(self):
        cs = CodeScanning()
        alert = CodeAlert(0, "open", "", {}, {})

    def test_codeql(self):
        codeql = CodeQL("codeql")
        alerts = CodeQLResults()

        dataext = DataExtensions("python")

        pack = CodeQLPack()
        packs = CodeQLPacks()

    def test_secretscanning(self):
        ss = SecretScanning()
        alert = SecretAlert(
            0, "open", "", "geekmasher_token", "GeekMasher Token", "ABCD"
        )

    def test_licenses(self):
        l = Licenses()
