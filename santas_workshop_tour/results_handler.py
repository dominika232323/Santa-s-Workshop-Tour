from pathlib import Path

from santas_workshop_tour.config import Individual


def save_results(best_individual: Individual, time: float, path_to_save: Path, timestamp: str) -> None:
    write_float_to_text_file(time, path_to_save, timestamp)


def write_float_to_text_file(value: float, path_to_save: Path, timestamp: str) -> None:
    path_to_save.mkdir(parents=True, exist_ok=True)
    file_path = path_to_save / f"{timestamp}.txt"
    file_path.write_text(str(value))
