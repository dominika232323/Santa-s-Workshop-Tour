from pathlib import Path
from typing import Tuple, List, Dict
from enum import Enum

PROJ_ROOT = Path(__file__).resolve().parents[1]

DATA_DIR = PROJ_ROOT / "data"
FAMILY_DATA = DATA_DIR / "family_data.csv"

RESULTS_DIR = PROJ_ROOT / "results"
RESULTS_EVOLUTIONARY_ALGORITHM = RESULTS_DIR / "evolutionary_algorithm"
RESULTS_COMPARISONS = RESULTS_DIR / "comparisons"

DEFAULT_HYPERPARAMETRS_CONFIGS_PATH = PROJ_ROOT / "santas_workshop_tour" / "hyperparameters.json"

Individual = Tuple[List[int], Dict[int, int]]


class MutationVariant(Enum):
    EXPLORATORY = "exploratory"
    EXPLOITATIVE = "exploitative"
