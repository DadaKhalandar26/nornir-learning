"""Tasks for backing up device configuration using NAPALM.

This module fetches the running config from devices using the
`nornir_napalm` plugin and writes timestamped backups to the
`02_nornir-config-backup/backups` folder.
"""

from datetime import datetime
import os
from typing import Optional

from utils.logging_util import get_logger
from nornir.core.task import Task, Result
from nornir_napalm.plugins.tasks import napalm_get

log = get_logger("backup_config")

# Backups are stored under the package folder's ../backups directory.
backup_folder = os.path.abspath(os.path.normpath(os.path.join(os.path.dirname(__file__), "..", "backups")))


def _get_timestamped_path(hostname: str) -> str:
    """Return a timestamped file path for a given hostname.

    The path will be: <repo>/02_nornir-config-backup/backups/<hostname>/<hostname>_YYYY-mm-dd_HH-MM-SS.txt
    """
    now = datetime.now()
    backup_host_folder = os.path.join(backup_folder, hostname)
    filename = f"{hostname}_{now.strftime('%Y-%m-%d_%H-%M-%S')}.txt"
    return os.path.join(backup_host_folder, filename)


def _fetch_running_config(task: Task) -> Optional[str]:
    """Fetch the running config from the device via NAPALM.

    Returns the running-config text or None if it could not be retrieved.
    """
    log.debug("Fetching running config for %s", task.host.name)
    result = task.run(task=napalm_get, getters=["config"])
    try:
        # result is a MultiResult; the napalm_get result is the first entry
        napalm_res = result[0].result
        running = napalm_res.get("config", {}).get("running")
        if running is None:
            log.error("No running config returned for %s", task.host.name)
        return running
    except Exception as exc:
        log.exception("Failed to fetch running config for %s: %s", task.host.name, exc)
        return None


def _write_config(path: str, config_text: str) -> bool:
    """Write `config_text` to `path`, creating parent directories as needed.

    Returns True on success, False on failure.
    """
    try:
        parent = os.path.dirname(path)
        os.makedirs(parent, exist_ok=True)
        with open(path, mode="w", encoding="utf-8") as f:
            f.write(config_text or "")
        log.debug("Wrote config to %s", path)
        return True
    except Exception as exc:
        log.exception("Failed to write config to %s: %s", path, exc)
        return False


def backup_config(task: Task) -> Result:
    """Nornir task that fetches a device running-config and saves it to disk.

    Returns a `Result` with `changed=True` and a message containing the
    saved path. Raises an exception to mark the task as failed when
    fetching or writing the config fails.
    """
    hostname = task.host.name
    running = _fetch_running_config(task=task)
    if running is None:
        raise Exception(f"Failed to fetch running config for {hostname}")

    out_path = _get_timestamped_path(hostname)
    success = _write_config(out_path, running)
    if not success:
        raise Exception(f"Failed to write backup for {hostname} to {out_path}")

    return Result(host=task.host, result=f"saved -> {out_path}", changed=True)


if __name__ == "__main__":
    from nornir import InitNornir
    from rich import print as r_print
    nr = InitNornir(config_file='config.yaml')
    filter_nr = nr.filter(name='site1-spine1')
    backup = filter_nr.run(task=backup_config)
    print(backup["site1-spine1"][0].diff)
    print(backup["site1-spine1"][0].name)
    print(backup["site1-spine1"][0].host)
    print(backup["site1-spine1"][0].failed)
    print(backup["site1-spine1"][0].exception)
    print(backup["site1-spine1"][0].result)