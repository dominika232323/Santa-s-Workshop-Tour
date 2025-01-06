from loguru import logger
from pathlib import Path

from santas_workshop_tour.config import Individual


def save_results(best_individual: Individual, time: float, path_to_save: Path) -> None:
    write_time_to_text_file(time, path_to_save)


def write_time_to_text_file(time: float, path_to_save: Path) -> None:
    path_to_save.mkdir(parents=True, exist_ok=True)

    file_path = path_to_save / f"time.txt"

    logger.info(f"Writing time ({time:.4f} secs) to text file at {file_path}")
    file_path.write_text(str(time))
