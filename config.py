import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "logs")

KEEP_DAYS = 7
INTERVAL = 1

# Display settings
GRAPH_WIDTH = 30

# Temperature thresholds (°C)
TEMP_NORMAL_MAX = 60
TEMP_WARM_MAX = 75
TEMP_HOT_MAX = 90
