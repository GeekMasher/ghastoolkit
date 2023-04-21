
import unittest

from ghastoolkit.octokit.dependencygraph import Dependency, Dependencies

class TestDepGraph(unittest.TestCase):
    def test_dependency(self):
        dep = Dependency("django", version="1.11.1", manager="pypi")

        self.assertEqual(dep.name, "django")
        self.assertEqual(dep.manager, "pypi")
        self.assertEqual(dep.version, "1.11.1")


    def test_purl(self):
        # python
        dep = Dependency("django", version="1.11.1", manager="pypi")
        self.assertEqual(dep.getPurl(), "pkg:pypi/django@1.11.1")
        
        # go
        dep = Dependency("genproto", "google.golang.org", manager="golang")
        self.assertEqual(dep.getPurl(), "pkg:golang/google.golang.org/genproto")

