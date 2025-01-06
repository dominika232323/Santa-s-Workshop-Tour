from datetime import datetime
from pathlib import Path

import typer
from loguru import logger

from santas_workshop_tour.config import RESULTS_COMPARISONS
from santas_workshop_tour.files_io import read_json, read_value_from_txt_file, save_dict_to_json
from santas_workshop_tour.results_handler import is_result_valid, get_result_score

app = typer.Typer()


@app.command()
def main(results: list[Path]):
    current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.info(f"Current timestamp: {current_timestamp}")

    scores = {}
    best_result_path = None
    best_result_score = None

    for result_path in results:
        people_per_day_dict = read_json(result_path / "people_per_day.json")

        if is_result_valid(people_per_day_dict):
            fitness_function_value = read_value_from_txt_file(result_path / "fitness_function_value.txt")
            time = read_value_from_txt_file(result_path / "time.txt")

            result_score = get_result_score(fitness_function_value, time)
            scores[str(result_path)] = result_score

            if best_result_path is None or result_score > best_result_score:
                best_result_path = result_path
                best_result_score = result_score

    save_dict_to_json(scores, RESULTS_COMPARISONS / current_timestamp / "scores.json")

    best_result = {best_result_path: best_result_score}
    save_dict_to_json(best_result, RESULTS_COMPARISONS / current_timestamp / "best_result.json")


if __name__ == "__main__":
    app()
