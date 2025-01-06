from pathlib import Path
from typing import Tuple, List, Dict
from enum import Enum

PROJ_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJ_ROOT / "data"
FAMILY_DATA = DATA_DIR / "family_data.csv"
Individual = Tuple[List[int], Dict[int, int]]


class MutationVariant(Enum):
    EXPLORATORY = "exploratory"
    EXPLOITATIVE = "exploitative"
