
import unittest

from ghastoolkit import Dependencies, Dependency, Licenses


class TestDependencies(unittest.TestCase):
    def setUp(self) -> None:
        self.deps = Dependencies()
        self.deps.append(Dependency("urllib3", manager="pypi", license="MIT"))
        self.deps.append(Dependency("rich", manager="pypi", license="NOASSERTION"))
        self.deps.append(Dependency("pyyaml", manager="pypi", license="GPL-3.0"))
        self.deps.append(Dependency("pyproject-hooks", manager="pypi", license="Apache-2.0"))
        self.deps.append(Dependency("requests", manager="pypi", license="GPL-2.0"))
        return super().setUp()

    def test_license(self):
        mit = self.deps.findLicenses(["MIT"])
        self.assertEqual(len(mit), 1)
        self.assertTrue(isinstance(self.deps.pop("urllib3"), Dependency))

        gpl = self.deps.findLicenses(["GPL-3.0", "GPL-2.0"])
        self.assertEqual(len(gpl), 2)
        self.assertTrue(isinstance(self.deps.pop("pyyaml"), Dependency))
        self.assertTrue(isinstance(self.deps.pop("requests"), Dependency))

    def test_license_wildcard(self):
        gpl = self.deps.findLicenses(["GPL-*"])
        self.assertEqual(len(gpl), 2)
        self.assertTrue(isinstance(self.deps.pop('pyyaml'), Dependency))
        self.assertTrue(isinstance(self.deps.pop('requests'), Dependency))

    def test_findName(self):
        pys = self.deps.findNames(["py*"])
        self.assertEqual(len(pys), 2)
        self.assertTrue(isinstance(self.deps.pop("pyyaml"), Dependency))
        self.assertTrue(isinstance(self.deps.pop("pyproject-hooks"), Dependency))

    def test_find(self):
        dep = self.deps.find("pyyaml")
        self.assertIsNotNone(dep)
        assert dep is not None
        self.assertEqual(dep.name, "pyyaml")

    def test_apply_license(self):
        deps = self.deps.findUnknownLicenses()
        self.assertEqual(len(deps), 1)

        licenses = Licenses()
        licenses.add("pkg:pypi/rich", ["MIT"])

        self.deps.applyLicenses(licenses)
        
        deps = self.deps.findUnknownLicenses()
        self.assertEqual(len(deps), 0)

        dep = self.deps.find("rich")
        self.assertEqual(dep.name, "rich")
        self.assertEqual(dep.license, "MIT")

    def test_update_dep(self):
        dep = Dependency("urllib3", manager="pypi", license="Apache-2")

        self.deps.updateDependency(dep)

        urllib_dep = self.deps.find("urllib3")
        self.assertEqual(urllib_dep.name, "urllib3")
        self.assertEqual(urllib_dep.license, "Apache-2")

    def test_hashable(self):
        dep = Dependency("urllib3", manager="pypi", license="MIT")
        self.assertEqual(hash(dep), hash(dep.getPurl()))

    def test_contains(self):
        dep = Dependency("urllib3", manager="pypi", license="MIT")
        self.assertTrue(self.deps.contains(dep))

        dep = Dependency("random-lib", manager="pypi", license="MIT")
        self.assertFalse(self.deps.contains(dep))
        
        # version is ignored
        dep = Dependency("urllib3", manager="pypi", license="MIT", version="1.26.5")
        self.assertTrue(self.deps.contains(dep))

        self.assertFalse(self.deps.contains(dep, version=True))
