import typer

from datetime import datetime
from loguru import logger
from pathlib import Path
from typing import Optional
from typing_extensions import Annotated
from rich.progress import track

from results_analysis.files_io import read_json
from santas_workshop_tour.config import FAMILY_DATA, RESULTS_EVOLUTIONARY_ALGORITHM, DEFAULT_HYPERPARAMETRS_CONFIGS_PATH
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.evolutionary_algorithm import EvolutionaryAlgorithm
from results_analysis.results_handler import save_result


def main(hyperparameters_configs_path: Annotated[Optional[Path], typer.Argument()] = None):
    if hyperparameters_configs_path is None:
        hyperparameters_configs_path = DEFAULT_HYPERPARAMETRS_CONFIGS_PATH

    logger.info(f"Loading hyperparameters from {hyperparameters_configs_path}")

    configs_list = read_json(hyperparameters_configs_path)

    for hyperparameters in track(configs_list, description="Processing..."):
        current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        logger.info(f"Current timestamp: {current_timestamp}")

        grabber = DataGrabber(FAMILY_DATA)

        algorithm = EvolutionaryAlgorithm(
            grabber,
            hyperparameters.get("crossover_probability"),
            hyperparameters.get("mutation_probability"),
            hyperparameters.get("family_mutation_probability"),
            hyperparameters.get("parents"),
            hyperparameters.get("elite_size"),
        )
        results, time = algorithm(hyperparameters.get("generations"), hyperparameters.get("population_size"))

        best_individual = results[0]
        population_statistics = results[1]
        best_individuals_fitness_values = results[2]
        penalties_by_generation = results[3]

        result_path = RESULTS_EVOLUTIONARY_ALGORITHM / current_timestamp
        logger.info(f"Saving results to {result_path}")
        save_result(best_individual, population_statistics, best_individuals_fitness_values, time, result_path, hyperparameters, penalties_by_generation)


if __name__ == '__main__':
    typer.run(main)
