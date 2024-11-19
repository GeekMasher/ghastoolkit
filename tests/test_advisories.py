import unittest
from ghastoolkit.supplychain.advisories import (
    Advisory,
    Advisories,
    AdvisoryAffect,
    parseVersion,
)
from ghastoolkit.supplychain.dependencies import Dependency


class TestAdvisories(unittest.TestCase):
    def setUp(self) -> None:
        self.advisories = Advisories()
        return super().setUp()

    def test_advisories(self):
        ad = Advisory("rand", "high")
        self.advisories.append(ad)
        self.assertEqual(len(self.advisories), 1)

    def test_advisory_check(self):
        affected = [
            AdvisoryAffect(
                "maven", "com.geekmasher.ghastoolkit", introduced="0", fixed="1"
            )
        ]
        ad = Advisory("rand", "high", affected=affected)
        self.advisories.append(ad)
        self.assertEqual(len(self.advisories), 1)

        dep = Dependency("ghastoolkit", "com.geekmasher", "0.8", "maven")

        alert = self.advisories.check(dep)
        self.assertEqual(alert, [ad])

    def test_advisory_cwes(self):
        ad = Advisory("rand", "high", cwes=["CWE-1234"])
        self.assertEqual(ad.cwes, ["CWE-1234"])

        ad = Advisory("rand", "high", cwes=[{"cwe_id": "CWE-1234"}])
        self.assertEqual(ad.cwes, ["CWE-1234"])

    def test_advisory_cvss(self):
        ad = Advisory(
            "rand",
            "high",
            cvss={
                "vector_string": "CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H",
                "score": 7.6
            }
        )
        self.assertEqual(ad.cvss_score(), 7.6)

        ad = Advisory(
            "rand",
            "high",
            cvss_severities={
                "cvss_v3": {
                    "vector_string": "CVSS:3.1/AV:N/AC:H/PR:H/UI:R/S:C/C:H/I:H/A:H",
                    "score": 7.6
                },
                "cvss_v4": {
                    "vector_string": "CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:N/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N",
                    "score": 9.3
                }
            }
        )
        self.assertEqual(ad.cvss_score(3), 7.6)
        self.assertEqual(ad.cvss_score(4), 9.3)

    def test_affect_check(self):
        dep = Dependency("ghastoolkit", "com.geekmasher", "0.8", "maven")
        affect = AdvisoryAffect(
            "maven", "com.geekmasher.ghastoolkit", introduced="0", fixed="1"
        )

        self.assertTrue(affect.check(dep))

    def test_post_init(self):
        affect = AdvisoryAffect(
            "maven", "com.geekmasher.ghastoolkit", introduced="0", fixed="1"
        )
        self.assertIsNotNone(affect.introduced)
        self.assertIsNotNone(affect.fixed)
        if affect.package_dependency:
            self.assertEqual(affect.package_dependency.name, "ghastoolkit")
            self.assertEqual(affect.package_dependency.namespace, "com.geekmasher")
        else:
            self.assertIsNotNone(affect.package_dependency)

        affect = AdvisoryAffect("pypi", "ghastoolkit", introduced="0", fixed="1")
        if affect.package_dependency:
            self.assertEqual(affect.package_dependency.name, "ghastoolkit")
            self.assertIsNone(affect.package_dependency.namespace)
        else:
            self.assertIsNotNone(affect.package_dependency)

    def test_affect_check_version(self):
        affect = AdvisoryAffect("", "", introduced="0.2", fixed="1")

        # too early
        self.assertFalse(affect.checkVersion("0.1"))
        self.assertFalse(affect.checkVersion("0.1.1"))
        # inside range
        self.assertTrue(affect.checkVersion("0.2"))
        self.assertTrue(affect.checkVersion("0.4.2"))
        self.assertTrue(affect.checkVersion("0.1111"))

        # fixed
        self.assertFalse(affect.checkVersion("1"))
        # later versions
        self.assertFalse(affect.checkVersion("1.1"))
        self.assertFalse(affect.checkVersion("10"))

    def test_parse_version(self):
        self.assertEqual(parseVersion("1"), "1.0.0")
        self.assertEqual(parseVersion("1.0"), "1.0.0")
        self.assertEqual(parseVersion("1.1.1"), "1.1.1")

    def test_affect_versions(self):
        affect = AdvisoryAffect("", "", introduced="0.2", fixed="1")
        self.assertEqual(affect.introduced, "0.2.0")
        self.assertEqual(affect.fixed, "1.0.0")
