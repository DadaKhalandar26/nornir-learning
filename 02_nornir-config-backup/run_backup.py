"""Entry point to run configuration backups for inventory devices.

This script initializes Nornir, filters devices in the `backup`
group, and runs the `backup_config` task on them. Results are logged
and the aggregated result object is returned.
"""

from utils.logging_util import get_logger
from nornir import InitNornir
from nornir.core.filter import F
import os
from dotenv import load_dotenv
try:
    # When executed as a package module this relative import works
    from .tasks.backup_config import backup_config  # type: ignore
except Exception:
    # Fallback for running the script directly from the folder
    from tasks.backup_config import backup_config

log = get_logger("run_backup")

load_dotenv(override=True)


def init_nornir():
    """Load Nornir from `config.yaml` and inject credentials from env.

    Expects `NORNIR_USERNAME` and `NORNIR_PASSWORD` to be set in the
    environment (or in a .env file loaded by python-dotenv).
    """
    nr = InitNornir(config_file="config.yaml")
    nr.inventory.defaults.username = os.getenv("NORNIR_USERNAME")
    nr.inventory.defaults.password = os.getenv("NORNIR_PASSWORD")
    return nr


def main():
    """Run the backup job for hosts in the `backup` group.

    Returns the aggregated Nornir result object.
    """
    try:
        nr = init_nornir()
        backup_device = nr.filter(F(groups__contains="backup"))
        log.info("Starting backup job for %d hosts", len(backup_device))
        backup_result = backup_device.run(task=backup_config)

        for host, multi_result in backup_result.items():
            try:
                res = multi_result[0]
            except Exception:
                log.error("Device %s: unexpected result structure", host)
                continue

            if getattr(res, "failed", False):
                log.error("Device %s: backup failed: %s", host, getattr(res, "exception", None))
                continue

            log.info("Device %s: backup saved: %s", host, getattr(res, "result", ""))

        return backup_result
    except Exception as e:
        log.exception("Backup job failed: %s", e)


if __name__ == "__main__":
    main()