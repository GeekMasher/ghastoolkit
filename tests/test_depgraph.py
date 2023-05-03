import unittest

from ghastoolkit.octokit.dependencygraph import Dependency, Dependencies


class TestDepGraph(unittest.TestCase):
    def test_dependency(self):
        dep = Dependency("django", version="1.11.1", manager="pypi")

        self.assertEqual(dep.name, "django")
        self.assertEqual(dep.manager, "pypi")
        self.assertEqual(dep.version, "1.11.1")

    def test_fullname_maven(self):
        dep = Dependency("express", manager="npm")
        self.assertEqual(dep.fullname, "express")

        dep = Dependency(
            "spring-boot-starter-web", "org.springframework.boot", manager="maven"
        )
        self.assertEqual(
            dep.fullname, "org.springframework.boot:spring-boot-starter-web"
        )

    def test_purl(self):
        # python
        dep = Dependency("django", version="1.11.1", manager="pypi")
        self.assertEqual(dep.getPurl(), "pkg:pypi/django@1.11.1")

        # go
        dep = Dependency("genproto", "google.golang.org", manager="golang")
        self.assertEqual(dep.getPurl(), "pkg:golang/google.golang.org/genproto")

    def test_purl_from(self):
        # GitHub Actions
        dep = Dependency.fromPurl("pkg:githubactions/actions/setup-python@3")
        self.assertEqual(dep.name, "setup-python")
        self.assertEqual(dep.namespace, "actions")
        self.assertEqual(dep.manager, "githubactions")
        self.assertEqual(dep.version, "3")

        dep = Dependency.fromPurl("pkg:githubactions/github/codeql-action/analyze@2")
        self.assertEqual(dep.name, "codeql-action/analyze")
        self.assertEqual(dep.namespace, "github")
        self.assertEqual(dep.manager, "githubactions")
        self.assertEqual(dep.version, "2")

        # PyPi
        dep = Dependency.fromPurl("pkg:pypi/requests@2.28.2")
        self.assertEqual(dep.name, "requests")
        self.assertEqual(dep.manager, "pypi")
        self.assertEqual(dep.version, "2.28.2")

    def test_purl_from_basic(self):
        dep = Dependency.fromPurl("npm/ini")
        self.assertEqual(dep.name, "ini")
        self.assertEqual(dep.manager, "npm")


class TestDependencies(unittest.TestCase):
    def setUp(self) -> None:
        self.deps = Dependencies()
        self.deps.append(Dependency("urllib3", licence="MIT"))
        self.deps.append(Dependency("rich", licence="NOASSERTION"))
        self.deps.append(Dependency("pyyaml", licence="GPL-3.0"))
        self.deps.append(Dependency("pyproject-hooks", licence="Apache-2.0"))
        self.deps.append(Dependency("requests", licence="GPL-2.0"))
        return super().setUp()

    def test_license(self):
        mit = self.deps.findLicenses(["MIT"])
        self.assertEqual(len(mit), 1)
        self.assertEqual(mit[0].name, "urllib3")

        gpl = self.deps.findLicenses(["GPL-3.0", "GPL-2.0"])
        self.assertEqual(len(gpl), 2)
        self.assertEqual(gpl[0].name, "pyyaml")
        self.assertEqual(gpl[1].name, "requests")

    def test_license_wildcard(self):
        gpl = self.deps.findLicenses(["GPL-*"])
        self.assertEqual(len(gpl), 2)
        self.assertEqual(gpl[0].name, "pyyaml")
        self.assertEqual(gpl[1].name, "requests")

    def test_findName(self):
        pys = self.deps.findNames(["py*"])
        self.assertEqual(len(pys), 2)
        self.assertEqual(pys[0].name, "pyyaml")
        self.assertEqual(pys[1].name, "pyproject-hooks")

    def test_find(self):
        dep = self.deps.find("pyyaml")
        self.assertIsNotNone(dep)
        assert dep is not None
        self.assertEqual(dep.name, "pyyaml")
