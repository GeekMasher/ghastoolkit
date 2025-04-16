"""GitHub Instance example."""

from ghastoolkit import GitHub

GitHub.init(
    repository="GeekMasher/ghastoolkit",
)

print(f"GitHub Repository  :: {GitHub.repository}")

# By default, the GitHub instance is set to https://github.com
print(f"GitHub Instance    :: {GitHub.instance}")
print(f"GitHub API REST    :: {GitHub.api_rest}")
print(f"GitHub API GraphQL :: {GitHub.api_graphql}")

# Initialise the GitHub will also load defaults values for access GitHub
# resources
if token := GitHub.getToken():
    # Only show the first 5 characters of the token
    print(f"GitHub Token       :: {token}    [masked for security]")
else:
    print("GitHub Token       :: Not set")
