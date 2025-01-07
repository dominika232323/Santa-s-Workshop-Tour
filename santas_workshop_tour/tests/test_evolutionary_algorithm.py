import pytest

from santas_workshop_tour.evolutionary_algorithm import EvolutionaryAlgorithm
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.config import FAMILY_DATA, MutationVariant
from unittest.mock import MagicMock


@pytest.fixture
def data_grabber():
    path_to_data = FAMILY_DATA
    return DataGrabber(path_to_data, sep=",")


@pytest.fixture
def algorithm(mock_family_data, data_grabber):
    return EvolutionaryAlgorithm(
        family_data=data_grabber,
        crossover_probability=0.7,
        mutation_probability=0.05,
        family_mutation_probability=0.02,
        parents=5,
        elite_size=5,
    )


@pytest.fixture
def mock_family_data():
    mock = MagicMock()
    mock.get_family_size.return_value = 4
    mock.get_family_choices.side_effect = lambda family_id: [1, 2, 3, 4, 5]
    return mock


def test_create_population(algorithm):
    population = algorithm.create_population(10)
    assert len(population) == 10
    assert len(population[6]) == 2


# def test_visitors_count_equals_families_count(data_grabber, algorithm):
#     population = algorithm.create_population(1)
#     visitors_count_sum = sum(sum(ind[1].values()) for ind in population)
#     families_counts_sum = sum(data_grabber.get_family_size(i) for i in range(5000))
#     assert visitors_count_sum == families_counts_sum


# def test_mutation(algorithm, mock_family_data):
#     individual = ([1, 2, 3, 4, 5], {day: 0 for day in range(1, 101)})
#     mutated_ind = algorithm.mutation(individual, MutationVariant.EXPLORATORY)
#     assert mutated_ind is not None
#     assert isinstance(mutated_ind, tuple)
#     assert len(mutated_ind[0]) == len(individual[0])


# def test_single_point_crossover(algorithm):
#     ind1 = ([1, 2, 3, 4, 5], {day: 0 for day in range(1, 101)})
#     ind2 = ([6, 7, 8, 9, 10], {day: 0 for day in range(1, 101)})

#     new_ind1, new_ind2 = algorithm.single_point_crossover(ind1, ind2)
#     assert isinstance(new_ind1, tuple)
#     assert isinstance(new_ind2, tuple)
#     assert len(new_ind1[0]) == len(ind1[0])
#     assert len(new_ind2[0]) == len(ind2[0])


# def test_elite_selection(algorithm):
#     population = [([1, 2, 3], {day: 0 for day in range(1, 101)}) for _ in range(50)]
#     offspring = [([4, 5, 6], {day: 0 for day in range(1, 101)}) for _ in range(50)]
#     next_gen = algorithm.elite_selection(population, offspring, S=10)
#     assert len(next_gen) == len(population)


# def test_setup_evolution(algorithm):
#     algorithm.setup_evolution()
#     assert "mutate" in algorithm.toolbox.__dict__
#     assert "mate" in algorithm.toolbox.__dict__
#     assert "evaluate" in algorithm.toolbox.__dict__
#     assert "succession" in algorithm.toolbox.__dict__
#     assert "select" in algorithm.toolbox.__dict__
