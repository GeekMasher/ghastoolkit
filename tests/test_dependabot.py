import unittest

import responses
import utils
from ghastoolkit import Dependabot, Dependency, DependencyAlert, Advisory

class TestDependabot(unittest.TestCase):

    @responses.activate
    def test_api(self):
        utils.loadResponses("dependabot.json", "alerts")
        dependabot = Dependabot()

        alerts = dependabot.getAlerts("open")

        self.assertEqual(len(alerts), 2)

        alert1 = alerts[0]
        self.assertIsInstance(alert1, DependencyAlert)
        self.assertIsInstance(alert1.advisory, Advisory)

        # EPSS
        self.assertIsInstance(alert1.advisory.epss, list)
        self.assertIsInstance(alert1.advisory.epss_percentage, float)
        self.assertEqual(alert1.advisory.epss_percentage, 0.00045)
        self.assertIsInstance(alert1.advisory.epss_percentile, str)
        self.assertEqual(alert1.advisory.epss_percentile, "0.16001e0")
