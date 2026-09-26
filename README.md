# temper-script

A lightweight terminal tool for real-time monitoring of CPU and NVMe/SSD temperatures on Linux, with logging and a live graph display powered by [Rich](https://github.com/Textualize/rich).

## Features

- **CPU temperature** — reads core/package temps via `psutil`
- **SSD/NVMe temperature** — reads drive temps via `smartctl`
- **Live table view** — updates in-place in the terminal (1x per second by default)
- **Sparkline-style graphs** — recent temperature history rendered as block-character graphs, with moving-average smoothing
- **CSV logging** — temperatures are logged per device, per day, under `logs/`
- **Automatic log rotation** — logs older than `KEEP_DAYS` are deleted on startup

## Requirements

- Linux
- Python 3
- Root privileges (required to read sensor/SMART data)
- [`smartmontools`](https://www.smartmontools.org/) installed (provides the `smartctl` command)
- Python packages: `psutil`, `rich`

Install dependencies:

```bash
pip install -r requirements.txt
sudo dnf install smartmontools
```

## Usage

Run as root:

```bash
sudo python3 main.py
```

Press `Ctrl+C` to stop monitoring.

## Configuration

Settings can be changed in `config.py`:

| Variable      | Description                                | Default |
|---------------|---------------------------------------------|---------|
| `LOG_DIR`     | Directory where CSV logs are stored          | `./logs` |
| `KEEP_DAYS`   | Number of days to keep old log files         | `7`     |
| `INTERVAL`    | Refresh interval in seconds                  | `1`     |
| `GRAPH_WIDTH` | Width of the graph in the table              | `30`    |

## Project Structure

```
.
├── main.py         # Entry point; runs the live monitoring loop
├── collectors.py    # Collects CPU and SSD/NVMe temperatures
├── logger.py         # Handles CSV log writing, reading, and rotation
├── display.py        # Renders the Rich table and graph
└── config.py          # Configuration constants
```

## Notes

- The tool must be run as root, since reading CPU sensors and SMART data typically requires elevated privileges.
- Log files are named `<device>_<YYYY-MM-DD>.csv` and stored under `logs/`.
