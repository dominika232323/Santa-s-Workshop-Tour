import numpy as np


def get_population_statistics(population):
    fitness_values = [ind.fitness.values[0] for ind in population if ind.fitness.valid]

    mean = np.mean(fitness_values)
    std_dev = np.std(fitness_values)
    min_value = np.min(fitness_values)
    max_value = np.max(fitness_values)

    return mean, std_dev, min_value, max_value


def get_statistics(population_statistics: list[tuple[float, float, float, float]]) -> tuple[list[float], list[float], list[float], list[float]]:
    mean_values = []
    std_dev_values = []
    min_values = []
    max_values = []

    for stats in population_statistics:
        mean_values.append(stats[0])
        std_dev_values.append(stats[1])
        min_values.append(stats[2])
        max_values.append(stats[3])

    return mean_values, std_dev_values, min_values, max_values
