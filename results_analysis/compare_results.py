from datetime import datetime
from pathlib import Path

import typer
from loguru import logger

from results_analysis.generate_plots import generate_boxplot, generate_comparison_plot_multiple_y_axes
from santas_workshop_tour.config import RESULTS_COMPARISONS, RESULTS_EVOLUTIONARY_ALGORITHM
from results_analysis.files_io import read_json, save_dict_to_json, find_subdirectories
from results_analysis.results_handler import is_result_valid, get_result_score, get_time_result, \
    get_fitness_value_result


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
    fitness_values = []

    for result_path in results:
        try:
            people_per_day_dict = read_json(result_path / "people_per_day.json")

            if is_result_valid(people_per_day_dict):
                fitness_function_value = get_fitness_value_result(result_path)
                fitness_values.append(fitness_function_value)

                time = get_time_result(result_path)
                runtimes.append(time)

                result_score = get_result_score(fitness_function_value, time)
                scores[str(result_path)] = result_score

                if best_result_path is None or result_score > best_result_score:
                    best_result_path = result_path
                    best_result_score = result_score
        except FileNotFoundError:
            logger.warning(f"Result files not found at {result_path}")

    save_dict_to_json(scores, RESULTS_COMPARISONS / current_timestamp / "scores.json")

    best_result = {str(best_result_path): best_result_score}
    save_dict_to_json(best_result, RESULTS_COMPARISONS / current_timestamp / "best_result.json")

    generate_boxplot(
        runtimes,
        results,
        RESULTS_COMPARISONS / current_timestamp / "runtime_distribution.png",
        "Rozkład czasu wykonywania",
        "Czas (s)"
    )

    generate_boxplot(
        fitness_values,
        results,
        RESULTS_COMPARISONS / current_timestamp / "fitness_value_distribution.png",
        "Rozkład wartości funkcji celu",
        "Wartość funkcji celu"
    )

    generate_comparison_plot_multiple_y_axes(
        runtimes,
        fitness_values,
        list(scores.values()),
        results,
        RESULTS_COMPARISONS / current_timestamp / "comparison_plot.png",
    )

if __name__ == "__main__":
    app()
