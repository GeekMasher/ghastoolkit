import os
import json
import logging
from typing import Any, Dict, Optional

logger = logging.getLogger("ghastoolkit.utils.cache")


class Cache:
    def __init__(self, root: Optional[str] = None, store: Optional[str] = None):
        """Initialize Cache."""
        if root is None:
            root = os.path.join(os.path.expanduser("~"), ".ghastoolkit", "cache")
        self.root = root
        self.store = store
        self.cache: Dict[str, Any] = {}

        logger.debug(f"Cache root: {self.root}")

        if not os.path.exists(self.cache_path):
            os.makedirs(self.cache_path, exist_ok=True)

    @property
    def cache_path(self) -> str:
        if self.store is None:
            return self.root
        return os.path.join(self.root, self.store)

    def read(self, key: str, file_type: Optional[str] = None) -> Optional[Any]:
        """Read from cache."""
        path = os.path.join(self.cache_path, key)
        if file_type:
            path = f"{path}.{file_type}"

        if os.path.exists(path):
            logger.debug(f"Cache hit: {path}")
            with open(path, "r") as file:
                return file.read()
        return None

    def write(self, key: str, value: Any, file_type: Optional[str] = None):
        """Write to cache."""
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        # Convert value to string if it's not already
        if isinstance(value, str):
            pass
        elif isinstance(value, dict):
            value = json.dumps(value)
        else:
            raise ValueError(f"Value is a unsupported type: {type(value)}")

        path = os.path.join(self.cache_path, key)
        # the key might be a owner/repo
        parent = os.path.dirname(path)
        if not os.path.exists(parent):
            os.makedirs(parent, exist_ok=True)

        if ftype := file_type:
            path = f"{path}.{ftype}"

        logger.debug(f"Cache write: {path}")
        with open(path, "w") as file:
            file.write(value)
