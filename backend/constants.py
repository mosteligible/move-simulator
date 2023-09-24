from enum import Enum
from pathlib import Path

DB_UPDATE_INTERVAL = 10  # seconds
ROOT_DIR = Path(__file__).absolute().parent
CONFIG_FILE_PATH = ROOT_DIR / "configuration.yaml"


class UnitConv(Enum):
    M_TO_KM = 1.0 / 1000.0
    KM_TO_M = 1000.0
