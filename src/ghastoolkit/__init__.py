__name__ = "ghastoolkit"
__title__ = "GHAS Toolkit"

__version__ = "0.1.11"

__description__ = "GitHub Advanced Security Python Toolkit"
__summary__ = """\
GitHub Advanced Security Python Toolkit
"""

__url__ = "https://github.com/GeekMasher/ghastoolkit"

__license__ = "MIT License"
__copyright__ = "Copyright (c) 2023, GeekMasher"

__author__ = "GeekMasher"

__banner__ = f"""\
 _____  _   _   ___   _____ _____           _ _    _ _   
|  __ \| | | | / _ \ /  ___|_   _|         | | |  (_) |  
| |  \/| |_| |/ /_\ \\\\ `--.  | | ___   ___ | | | ___| |_ 
| | __ |  _  ||  _  | `--. \ | |/ _ \ / _ \| | |/ / | __|
| |_\ \| | | || | | |/\__/ / | | (_) | (_) | |   <| | |_ 
 \____/\_| |_/\_| |_/\____/  \_/\___/ \___/|_|_|\_\_|\__| v{__version__} 
"""


# Octokit
from ghastoolkit.octokit.github import GitHub, Repository
from ghastoolkit.octokit.octokit import Octokit, RestRequest, GraphQLRequest
from ghastoolkit.octokit.codescanning import CodeScanning
from ghastoolkit.octokit.secretscanning import SecretScanning
from ghastoolkit.octokit.dependencygraph import (
    DependencyGraph,
    Dependencies,
    Dependency,
)

# CodeQL
from ghastoolkit.codeql.databases import CodeQLDatabases, CodeQLDatabase
