import numpy as np


def get_population_statistics(population):
    fitness_values = [ind.fitness.values[0] for ind in population if ind.fitness.valid]

    mean = np.mean(fitness_values)
    std_dev = np.std(fitness_values)
    min_value = np.min(fitness_values)
    max_value = np.max(fitness_values)

    return mean, std_dev, min_value, max_value
