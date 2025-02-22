from pathlib import Path
from typing import Any

from loguru import logger

from results_analysis.generate_plots import generate_line_plot, generate_statistics_plot
from santas_workshop_tour.config import Individual
from results_analysis.files_io import write_value_to_text_file, save_data_to_csv, save_dict_to_json, \
    read_value_from_txt_file


def save_result(
        best_individual: Individual,
        population_statistics: list[tuple[float, float, float, float]],
        best_individuals_fitness_values: list[float],
        time: float,
        path_to_save: Path,
        hyperparameters: dict[str, Any],
        penalties_by_generation: list[list[Any]]
) -> None:

    save_data_to_csv(best_individual[0], path_to_save / "assigned_days.csv", ["family_id", "assigned_day"])
    save_dict_to_json(best_individual[1], path_to_save / "people_per_day.json")

    generations = list(range(0, len(best_individuals_fitness_values)))

    save_data_to_csv(
        population_statistics,
        path_to_save / "population_statistics.csv",
        ["generation", "mean", "standard_deviation", "min_value", "max_value"]
    )
    generate_statistics_plot(
        generations,
        population_statistics,
        path_to_save / "statistics_plot.png",
    )

    save_data_to_csv(
        best_individuals_fitness_values,
        path_to_save / "best_individuals_fitness_values.csv",
        ["generation", "fitness_value"]
    )
    generate_line_plot(
        generations,
        best_individuals_fitness_values,
        "Generacja",
        "Wartości funkcji celu",
        "Zmiana wartości funkcji celu najlepszego osobnika od generacji",
        path_to_save / "best_individuals_fitness_values_plot.png"
    )

    write_value_to_text_file(best_individual.fitness.values[0], path_to_save / "fitness_function_value.txt")
    write_value_to_text_file(time, path_to_save / "time.txt")

    save_dict_to_json(hyperparameters, path_to_save / "hyperparameters.json")

    save_data_to_csv(
        penalties_by_generation,
        path_to_save / "penalties_by_generation.csv",
        ["generation", "individual", "restriction_penalty", "choice_penalty", "accounting_penalty", "fitness_value"],
        False
    )


def is_result_valid(people_per_day_dict: dict[str: int]) -> bool:
    for day, people_number in people_per_day_dict.items():
        if people_number < 125 or people_number > 300:
            logger.info(f"Result is invalid. Day {day} with number of visitors {people_number} is out of range.")
            return False

    return True


def get_result_score(fitness_function_value: float, time: float, weight_fitness: float = 0.7) -> float:
    if weight_fitness > 1 or weight_fitness < 0:
        raise ValueError(f"weight_fitness must be >= 0 and <= 1, got {weight_fitness}")

    weight_time = 1 - weight_fitness

    return fitness_function_value * weight_fitness + time * weight_time


def get_time_result(result_path: Path) -> float:
    return read_value_from_txt_file(result_path / "time.txt")


def get_fitness_value_result(result_path: Path) -> float:
    return read_value_from_txt_file(result_path / "fitness_function_value.txt")
