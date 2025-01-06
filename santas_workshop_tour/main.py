from datetime import datetime

from loguru import logger

from santas_workshop_tour.config import FAMILY_DATA, RESULTS_DIR
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.evolutionary_algorithm import EvolutionaryAlgorithm
from santas_workshop_tour.results_handler import save_result

if __name__ == '__main__':
    current_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logger.info(f"Current timestamp: {current_timestamp}")

    grabber = DataGrabber(FAMILY_DATA)
    algorithm = EvolutionaryAlgorithm(grabber, 0.7, 0.05, 0.02, 40, 30)
    best_individual, time = algorithm(2, 50)

    result_path = RESULTS_DIR / current_timestamp
    logger.info(f"Saving results to {result_path}")
    save_result(best_individual, time, result_path)
