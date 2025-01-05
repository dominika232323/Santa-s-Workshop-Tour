from deap import creator, base, tools
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.config import FAMILY_DATA
from santas_workshop_tour.individual import Individual


class EvolutionaryAlgorithm:
    def __init__(self) -> None:
        self.toolbox = None

    def create_population(self, family_choices: DataGrabber, N: int) -> list[Individual]:

        individual = Individual()
        self.toolbox = individual.create_toolbox(
            lambda: individual.init_individual(family_choices)
        )
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        return self.toolbox.population(n=N)


grabber = DataGrabber(FAMILY_DATA, sep=",")
algorithm = EvolutionaryAlgorithm()
population = algorithm.create_population(grabber, 10)
print(type(population[0]))
