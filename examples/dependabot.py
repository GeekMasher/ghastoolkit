"""Dependabot API example."""
import logging
from ghastoolkit import Dependabot, GitHub

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
GitHub.init("octodemo/demo-ghas-geekmasher")

# graphql = GraphQLRequest(GitHub.repository)
depgraph = Dependabot()

alerts = depgraph.getAlerts()
print(f"Total Alerts :: {len(alerts)}")
