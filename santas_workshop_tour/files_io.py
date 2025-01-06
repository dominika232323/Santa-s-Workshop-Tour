import csv
import json
from pathlib import Path

from loguru import logger


def write_value_to_text_file(value: float, path_to_txt: Path) -> None:
    path_to_txt.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Writing value ({value:.4f}) to text file at {path_to_txt}")
    path_to_txt.write_text(str(value))


def read_value_from_txt_file(path_to_txt: Path) -> float:
    path_to_txt.parent.mkdir(parents=True, exist_ok=True)

    with open(path_to_txt, "r") as file:
        return float(file.read())


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


def read_json(path_to_json: Path) -> dict:
    with open(path_to_json, mode="r") as file:
        data = json.load(file)

    return data
