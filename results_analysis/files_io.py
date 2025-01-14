import csv
import json
from pathlib import Path
from typing import Any

from loguru import logger


def write_value_to_text_file(value: float, path_to_txt: Path) -> None:
    path_to_txt.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Writing value ({value:.4f}) to text file at {path_to_txt}")
    path_to_txt.write_text(str(value))


def read_value_from_txt_file(path_to_txt: Path) -> float:
    path_to_txt.parent.mkdir(parents=True, exist_ok=True)

    with open(path_to_txt, "r") as file:
        return float(file.read())


def save_data_to_csv(data: list[Any], path_to_csv: Path, headers: list[str], write_index: bool = True) -> None:
    path_to_csv.parent.mkdir(parents=True, exist_ok=True)

    with path_to_csv.open(mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(headers)

        if isinstance(data, list):
            for index, value in enumerate(data):
                if isinstance(value, tuple):
                    row = [index] + list(value) if write_index else list(value)
                elif isinstance(value, list):
                    row = [index] + value if write_index else value
                else:
                    row = [index, value] if write_index else value

                writer.writerow(row)
        else:
            raise ValueError("Unsupported data type. Only lists, tuples, or nested lists are supported.")

    logger.info(f"Writing data to csv at {path_to_csv}")


def save_dict_to_json(data: dict, path_to_json: Path) -> None:
    path_to_json.parent.mkdir(parents=True, exist_ok=True)

    logger.info(f"Writing dict to json at {path_to_json}")

    with open(path_to_json, mode="w") as file:
        json.dump(data, file, indent=4)


def read_json(path_to_json: Path) -> dict:
    with open(path_to_json, mode="r") as file:
        data = json.load(file)

    return data


def find_subdirectories(directory: Path) -> list[Path]:
    return [subdir for subdir in directory.rglob('*') if subdir.is_dir()]
