
import unittest

from ghastoolkit.octokit.clearlydefined import ClearlyDefined
from ghastoolkit.supplychain.dependencies import Dependency


class TestClearly(unittest.TestCase):
    def test_url_builder(self):
        clearly = ClearlyDefined()
        dep = Dependency("requests", manager="pypi")

        url = clearly.createCurationUrl(dep)
        self.assertEqual(url, f"{clearly.api}/curations/pypi/pypi/-/requests")


