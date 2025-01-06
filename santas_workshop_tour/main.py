from santas_workshop_tour.config import FAMILY_DATA
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.evolutionary_algorithm import EvolutionaryAlgorithm


if __name__ == '__main__':
    grabber = DataGrabber(FAMILY_DATA)
    algorithm = EvolutionaryAlgorithm(grabber, 0.7, 0.05, 0.02, 40, 30)
    result, time = algorithm(2, 50)
    print(result)
    print(time)
