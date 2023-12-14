import os
from ghastoolkit import Advisories, Advisory, SecurityAdvisories
from ghastoolkit.octokit.github import GitHub
from ghastoolkit.supplychain.dependencies import Dependency

# Load GitHub
GitHub.init(
    os.environ.get("GITHUB_REPOSITORY", "GeekMasher/ghastoolkit"),
)
print(f"{GitHub.repository}")

# SecurityAdvisories REST API helper
security_advisories = SecurityAdvisories()

# get remote security advisories
advisories: Advisories = security_advisories.getAdvisories()
print(f"Remote Advisories :: {len(advisories)}")
# load local (json) advisories
advisories.loadAdvisories("./examples")

print(f"Total Advisories  :: {len(advisories)}")

for a in advisories.advisories:
    print(f"Advisory :: {a.ghsa_id} ({a.summary})")

# get log4shell advisory
log4shell: Advisory = advisories.find("ghas-jfh8-c2jp-5v3q")

if log4shell:
    print(f"Advisory :: {log4shell.ghsa_id} ({log4shell.summary})")

# load Dependency from PURL (log4j vulnerable to log4shell)
dependency = Dependency.fromPurl("pkg:maven/org.apache.logging/log4j:log4j-core@1.12.0")
print(f"Dependency :: {dependency.name} ({dependency.version})")

# display all advisories which affect the dependency
print("Advisories Found:")
for adv in advisories.check(dependency):
    print(f" >>> Advisory({adv.ghsa_id}, `{','.join(adv.aliases)}`)")
