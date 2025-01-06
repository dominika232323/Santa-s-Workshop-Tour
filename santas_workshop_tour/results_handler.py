import csv
import json

from loguru import logger
from pathlib import Path

from santas_workshop_tour.config import Individual


def save_results(best_individual: Individual, time: float, path_to_save: Path) -> None:
    save_list_to_csv(best_individual[0], path_to_save / "assigned_days.csv", ["family_id", "assigned_day"])
    save_dict_to_json(best_individual[1], path_to_save / "people_per_day.json")
    write_value_to_text_file(best_individual.fitness.values[0], path_to_save / "individual_value.txt")
    write_value_to_text_file(time, path_to_save / "time.txt")


def write_value_to_text_file(value: float, path_to_txt: Path) -> None:
    path_to_txt.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Writing value ({value:.4f}) to text file at {path_to_txt}")
    path_to_txt.write_text(str(value))


def save_list_to_csv(data: list[int], path_to_csv: Path, headers: list[str]) -> None:
    if len(headers) != 2:
        raise ValueError(f"Expected 2 headers, got {len(headers)}")

    path_to_csv.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Writing list to csv at {path_to_csv}")

    with path_to_csv.open(mode="w", newline="") as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        for family_id, assigned_day in enumerate(data):
            writer.writerow([family_id, assigned_day])


def save_dict_to_json(data: dict, path_to_json: Path) -> None:
    path_to_json.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Writing dict to json at {path_to_json}")

    with open(path_to_json, mode="w") as file:
        json.dump(data, file, indent=4)
