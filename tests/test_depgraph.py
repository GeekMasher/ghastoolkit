import unittest

from ghastoolkit.octokit.dependencygraph import Dependency, Dependencies
from ghastoolkit.supplychain.licensing import Licenses


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

