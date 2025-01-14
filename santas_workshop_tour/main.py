from datetime import datetime

from loguru import logger

from santas_workshop_tour.config import FAMILY_DATA, RESULTS_EVOLUTIONARY_ALGORITHM
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.evolutionary_algorithm import EvolutionaryAlgorithm
from results_analysis.results_handler import save_result

if __name__ == '__main__':
    current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.info(f"Current timestamp: {current_timestamp}")

    grabber = DataGrabber(FAMILY_DATA)

    hyperparameters = {
        "crossover_probability": 0.7,
        "mutation_probability": 0.05,
        "family_mutation_probability": 0.02,
        "parents": 40,
        "elite_size": 30,
        "generations": 2,
        "population_size": 50
    }

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


    result_path = RESULTS_EVOLUTIONARY_ALGORITHM / current_timestamp
    logger.info(f"Saving results to {result_path}")
    save_result(best_individual, population_statistics, best_individuals_fitness_values, time, result_path, hyperparameters)
