import unittest

from ghastoolkit import *


class TestDefault(unittest.TestCase):
    def test_supplychain(self):
        gp = DependencyGraph()
        deps = Dependencies()
        dep = Dependency("ghastoolkit")

        alert = DependencyAlert("high", Advisory("0000", "high"), "pypi/ghastoolkit")

    def test_codescanning(self):
        cs = CodeScanning()
        alert = CodeAlert(0, "open", "", {}, {})

    def test_secretscanning(self):
        ss = SecretScanning()
        alert = SecretAlert(
            0, "open", "", "geekmasher_token", "GeekMasher Token", "ABCD"
        )

    def test_licenses(self):
        l = Licenses()
