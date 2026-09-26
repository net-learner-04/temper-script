# temper-script

A lightweight terminal tool for real-time monitoring of CPU and NVMe/SSD temperatures on Linux, with CSV logging and a live temperature display powered by [Rich](https://github.com/Textualize/rich).

## Features

* **CPU temperature** — reads core/package temperatures via `psutil`
* **SSD/NVMe temperature** — reads drive temperatures via `smartctl`
* **Live temperature table** — updates device temperatures and status in-place in the terminal
* **Temperature status** — displays `NORMAL`, `WARM`, `HOT`, or `CRITICAL` based on configurable temperature thresholds
* **CSV logging** — temperatures are logged per device, per day, under `logs/`
* **Automatic log rotation** — logs older than `KEEP_DAYS` are deleted on startup

## Requirements

* Linux
* Python 3
* Root privileges (required to read sensor/SMART data)
* [`smartmontools`](https://www.smartmontools.org/) installed (provides the `smartctl` command)
* Python packages: `psutil`, `rich`

Install Python dependencies:

```bash
pip install -r requirements.txt
```

Install `smartmontools`:

```bash
sudo dnf install smartmontools
```

## Usage

Run the program as root:

```bash
sudo python3 main.py
```

Press `Ctrl+C` to stop monitoring.

## Configuration

Settings can be changed in `config.py`:

| Variable          | Description                          |  Default |
| ----------------- | ------------------------------------ | -------: |
| `LOG_DIR`         | Directory where CSV logs are stored  | `./logs` |
| `KEEP_DAYS`       | Number of days to keep old log files |      `7` |
| `INTERVAL`        | Refresh interval in seconds          |      `1` |
| `TEMP_NORMAL_MAX` | Upper limit for `NORMAL` status (°C) |     `60` |
| `TEMP_WARM_MAX`   | Upper limit for `WARM` status (°C)   |     `75` |
| `TEMP_HOT_MAX`    | Upper limit for `HOT` status (°C)    |     `90` |

Temperature status is determined as follows:

| Temperature     | Status     |
| --------------- | ---------- |
| `< 60°C`        | `NORMAL`   |
| `60°C – < 75°C` | `WARM`     |
| `75°C – < 90°C` | `HOT`      |
| `≥ 90°C`        | `CRITICAL` |

## Project Structure

```text
.
├── main.py         # Entry point; runs the live monitoring loop
├── collectors.py   # Collects CPU and SSD/NVMe temperatures
├── logger.py       # Handles CSV logging, reading, and log rotation
├── display.py      # Renders the Rich temperature table and status
└── config.py       # Configuration constants
```

## Logging

Temperature data is stored as CSV files under the `logs/` directory.

Each device has its own daily log file:

```text
logs/
├── cpu_thermal_2026-09-26.csv
├── nvme0_2026-09-26.csv
└── ...
```

Each CSV file contains the timestamp and temperature:

```csv
timestamp,temperature
2026-09-26 19:00:01,52.0
2026-09-26 19:00:02,53.0
2026-09-26 19:00:03,54.0
```

Logs older than `KEEP_DAYS` are automatically deleted when the program starts.

## Notes

* The tool must be run as root, since reading CPU sensors and SMART data typically requires elevated privileges.
* `smartmontools` must be installed for SSD/NVMe temperature detection.
* The display shows the current temperature and status for each detected device.
* Temperature thresholds can be adjusted in `config.py`.
