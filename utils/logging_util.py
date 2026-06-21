import logging
import sys

_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"
_configured = False


def setup_logging(level: int = logging.INFO) -> None:
    """Configure root logging once for the whole package."""
    global _configured
    if _configured:
        return
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(_FORMAT))
    root = logging.getLogger()
    root.setLevel(level)
    root.addHandler(handler)
    _configured = True


def get_logger(name: str) -> logging.Logger:
    """Return a module-scoped logger. Call as get_logger(__name__)."""
    setup_logging()
    return logging.getLogger(name)