
import unittest
from semantic_version import Version
from ghastoolkit.supplychain.advisories import Advisory, Advisories, AdvisoryAffect
from ghastoolkit.supplychain.dependencies import Dependency


class TestAdvisories(unittest.TestCase):
    def setUp(self) -> None:
        self.advisories = Advisories()
        return super().setUp()

    def test_advisories(self):
        ad = Advisory("rand", "high")
        self.advisories.append(ad)
        self.assertEquals(len(self.advisories), 1)

    def test_advisory_check(self):
        affected = [AdvisoryAffect("maven", "com.geekmasher.ghastoolkit", range_events={"introduced": "0", "fixed": "1"})]
        ad = Advisory("rand", "high", affected=affected)
        self.advisories.append(ad)
        self.assertEquals(len(self.advisories), 1)

        dep = Dependency("ghastoolkit", "com.geekmasher", "0.8", "maven")

        alert = self.advisories.check(dep)
        self.assertEquals(alert, ad)
        
    def test_affect_check(self):
        affect = AdvisoryAffect("", "", range_events={"introduced": "0", "fixed": "1"})

        self.assertTrue(affect.check("0.1"))
        self.assertTrue(affect.check("0.1.1"))
        self.assertTrue(affect.check("1"))

        self.assertFalse(affect.check("1.1"))
        self.assertFalse(affect.check("10"))



