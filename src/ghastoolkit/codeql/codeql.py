"""CodeQL Helper."""
import logging
from ghastoolkit.codeql.cli import CodeQL

logger = logging.getLogger("ghastoolkit.codeql")


class CodeQL:
    """CodeQL Helper"""

    def __init__(self) -> None:
        self.cli = CodeQLCli()
