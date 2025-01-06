from deap import tools
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.config import FAMILY_DATA, Individual, MutationVariant
from santas_workshop_tour.individual_factory import IndividualFactory
from santas_workshop_tour.cost_function import cost_function
from typing import Tuple
from functools import partial
import random


class EvolutionaryAlgorithm:
    def __init__(
        self,
        family_data: DataGrabber,
        crossover_probability: float,
        mutation_probability: float,
        family_mutation_probability: float,
        parents: int,
        elite_size: int,
    ) -> None:
        self.toolbox = None
        self.family_data = family_data
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.family_mutation_probability = family_mutation_probability
        self.parents = parents
        self.elite_size = elite_size

    def __call__(self, generations_num: int, N: int):
        population = self.create_population(N)
        self.setup_evolution()
        for gen in range(generations_num):
            offspring = self.toolbox.select(population, len(population))

            offspring = list(map(self.toolbox.clone, offspring))
            for parent1, parent2 in zip(offspring[::2], offspring[1::2]):
                roll = random.random()
                if roll < self.crossover_probability:
                    self.toolbox.mate(parent1, parent2)
                    del parent1.fitness.values
                    del parent2.fitness.values

            for ind in offspring:
                roll = random.random()
                if roll < self.mutation_probability:
                    self.toolbox.mutate(ind)
                    del ind.fitness.values

            invalid_ind = [ind for ind in offspring if not ind.fitness.values]
            fitnesses = map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(offspring, fitnesses):
                ind.fitness.values = fit

            population = self.toolbox.succession(population, offspring, S=self.elite_size)
            print(len(population))
            best_ind = tools.selBest(population, 1)[0]
            print(f"Generation {gen}: Best Fitness = {best_ind.fitness.values[0]}")

    def setup_evolution(self):
        self.toolbox.register("mutate", self.mutation, variant=MutationVariant.EXPLORATORY)
        self.toolbox.register("mate", self.single_point_crossover)
        self.toolbox.register("evaluate", partial(cost_function, family_choices=self.family_data))
        self.toolbox.register("succession", self.elite_selection)
        self.toolbox.register("select", tools.selTournament, tournsize=self.parents)

    def create_population(self, N: int) -> list[Individual]:

        individual = IndividualFactory()
        self.toolbox = individual.create_toolbox(
            lambda: individual.init_individual(self.family_data)
        )
        self.toolbox.register("population", tools.initRepeat, list, self.toolbox.individual)

        return self.toolbox.population(n=N)

    def mutation(self, individual, variant: MutationVariant) -> Individual:
        for family_id, visit_day in enumerate(individual[0]):
            roll = random.random()
            if roll < self.family_mutation_probability:
                if variant == MutationVariant.EXPLORATORY:
                    new_day = random.randint(1, 100)
                elif variant == MutationVariant.EXPLOITATIVE:
                    new_day = random.choice(self.family_data.get_family_choices(family_id))
                individual = self.change_visit_day(family_id, visit_day, new_day, individual)
        return (individual,)

    def change_visit_day(
        self, family_id: int, previous_day: int, new_day: int, individual: Individual
    ) -> Individual:
        visits_days, visitors_by_days = individual
        visitors_by_days[previous_day] -= self.family_data.get_family_size(family_id)
        visitors_by_days[new_day] += self.family_data.get_family_size(family_id)
        visits_days[family_id] = new_day
        return visits_days, visitors_by_days

    def single_point_crossover(
        self, individual_1: Individual, individual_2: Individual
    ) -> Tuple[Individual, Individual]:

        size = len(individual_1[0])
        cxpoint = random.randint(1, size - 1)

        ind1_left, ind1_right, ind2_left, ind2_right = self.split_individuals(
            individual_1, individual_2, cxpoint
        )

        self.update_visitors_by_days(individual_1, individual_2, ind1_right, ind2_right, cxpoint)

        new_individual_1 = (ind1_left + ind2_right, individual_1[1])
        new_individual_2 = (ind2_left + ind1_right, individual_2[1])

        return new_individual_1, new_individual_2

    def split_individuals(
        self, individual_1: Individual, individual_2: Individual, cxpoint: int
    ) -> list[list, list, list, list]:

        ind1_left = individual_1[0][:cxpoint]
        ind1_right = individual_1[0][cxpoint:]

        ind2_left = individual_2[0][:cxpoint]
        ind2_right = individual_2[0][cxpoint:]
        return ind1_left, ind1_right, ind2_left, ind2_right

    def update_visitors_by_days(
        self,
        individual_1: Individual,
        individual_2: Individual,
        ind1_right: list,
        ind2_right: list,
        cxpoint: int
    ) -> None:
        for family_id, day in enumerate(ind1_right, start=cxpoint):
            individual_1[1][day] -= self.family_data.get_family_size(family_id)
            individual_2[1][day] += self.family_data.get_family_size(family_id)

        for family_id, day in enumerate(ind2_right, start=cxpoint):
            individual_1[1][day] += self.family_data.get_family_size(family_id)
            individual_2[1][day] -= self.family_data.get_family_size(family_id)

    def elite_selection(
        self, population: list[Individual], offspring: list[Individual], S: int
    ) -> list[Individual]:
        elites = tools.selBest(population, S)
        remaining_slots = len(population) - S
        next_gen = elites + tools.selBest(offspring, remaining_slots)
        return next_gen


grabber = DataGrabber(FAMILY_DATA)
algorithm = EvolutionaryAlgorithm(grabber, 0.7, 0.05, 0.02, 40, 30)
algorithm(20, 100)