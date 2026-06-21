
02_nornir-config-backup
======================

What it does
-----------
- Collects running configuration from devices in the inventory that belong to the `backup` group using Nornir + NAPALM.
- Saves timestamped backups per-host under `02_nornir-config-backup/backups/<hostname>/`.

Requirements
------------
- Python 3.8+
- Dependencies listed in the repository `requirements.txt` (install with `pip install -r requirements.txt`).
- A properly configured `config.yaml` for Nornir and an inventory in the `inventory/` folder.

Environment
-----------
- Set `NORNIR_USERNAME` and `NORNIR_PASSWORD` environment variables (or place them in a `.env` file) so the script can authenticate to devices.

Usage
-----
Run the backup job:

- From the `02_nornir-config-backup` folder:

```powershell
python run_backup.py
```

- Or from the repository root (explicit path):

```powershell
python 02_nornir-config-backup\run_backup.py
```

Outputs
-------
- Backups are saved to `02_nornir-config-backup/backups/<hostname>/<hostname>_YYYY-mm-dd_HH-MM-SS.txt`.
- The script logs progress via the repository logging utility.

Notes
-----
- The backup task uses the `nornir_napalm.plugins.tasks.napalm_get` getter to retrieve the running configuration. Ensure the devices and NAPALM drivers are supported and reachable.
- If you want to change the backup folder location, update `backup_folder` in `tasks/backup_config.py`.

