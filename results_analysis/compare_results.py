from datetime import datetime
from pathlib import Path

import typer
from loguru import logger

from results_analysis.generate_plots import generate_boxplot
from santas_workshop_tour.config import RESULTS_COMPARISONS, RESULTS_EVOLUTIONARY_ALGORITHM
from results_analysis.files_io import read_json, read_value_from_txt_file, save_dict_to_json, find_subdirectories
from results_analysis.results_handler import is_result_valid, get_result_score, get_time_result

app = typer.Typer()




@app.command()
def main(results: list[Path] = typer.Argument(None, help="List of result directories")):
    current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.info(f"Current timestamp: {current_timestamp}")

    if not results:
        results = find_subdirectories(RESULTS_EVOLUTIONARY_ALGORITHM)

    scores = {}
    best_result_path = None
    best_result_score = None
    runtimes = []

    for result_path in results:
        people_per_day_dict = read_json(result_path / "people_per_day.json")

        if is_result_valid(people_per_day_dict):
            fitness_function_value = read_value_from_txt_file(result_path / "fitness_function_value.txt")
            time = get_time_result(result_path)
            runtimes.append(time)

            result_score = get_result_score(fitness_function_value, time)
            scores[str(result_path)] = result_score

            if best_result_path is None or result_score > best_result_score:
                best_result_path = result_path
                best_result_score = result_score

    save_dict_to_json(scores, RESULTS_COMPARISONS / current_timestamp / "scores.json")

    best_result = {str(best_result_path): best_result_score}
    save_dict_to_json(best_result, RESULTS_COMPARISONS / current_timestamp / "best_result.json")

    generate_boxplot(
        runtimes,
        results,
        RESULTS_COMPARISONS / current_timestamp / "runtimes.png",
        "Rozkład czasu wykonywania",
        "Czas (s)"
    )


if __name__ == "__main__":
    app()
