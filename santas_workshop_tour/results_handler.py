from pathlib import Path

from santas_workshop_tour.config import Individual
from santas_workshop_tour.files_io import write_value_to_text_file, save_list_to_csv, save_dict_to_json


def save_results(best_individual: Individual, time: float, path_to_save: Path) -> None:
    save_list_to_csv(best_individual[0], path_to_save / "assigned_days.csv", ["family_id", "assigned_day"])
    save_dict_to_json(best_individual[1], path_to_save / "people_per_day.json")
    write_value_to_text_file(best_individual.fitness.values[0], path_to_save / "fitness_function_value.txt")
    write_value_to_text_file(time, path_to_save / "time.txt")


def is_result_valid(path_to_result: Path) -> bool:
    pass


def get_result_score(fitness_function_value: float, time: float, weight_fitness: float = 0.7) -> float:
    if weight_fitness > 1 or weight_fitness < 0:
        raise ValueError(f"weight_fitness must be >= 0 and <= 1, got {weight_fitness}")

    weight_time = 1 - weight_fitness

    return fitness_function_value * weight_fitness + time * weight_time

