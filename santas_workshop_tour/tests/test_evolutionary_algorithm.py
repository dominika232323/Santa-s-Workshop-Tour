import pytest

from santas_workshop_tour.evolutionary_algorithm import EvolutionaryAlgorithm
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.config import FAMILY_DATA


@pytest.fixture
def data_grabber():
    path_to_data = FAMILY_DATA
    return DataGrabber(path_to_data, sep=",")


@pytest.fixture
def evolutionary_algorithm():
    return EvolutionaryAlgorithm()


def test_make_preferences_dict(data_grabber, evolutionary_algorithm):
    preferences_dict = evolutionary_algorithm.make_preferences_dict(data_grabber)
    assert preferences_dict[23] == data_grabber.get_family_choices(23)
    assert preferences_dict[778] == data_grabber.get_family_choices(778)
    assert preferences_dict[3241] == data_grabber.get_family_choices(3241)


def test_create_population(data_grabber, evolutionary_algorithm):
    population = evolutionary_algorithm.create_population(data_grabber, 10)
    assert len(population) == 10
    assert len(population[6]) == 2


def test_visitors_count_equals_families_count(data_grabber, evolutionary_algorithm):
    population = evolutionary_algorithm.create_population(data_grabber, 1)
    visitors_count_sum = sum(sum(ind[1].values()) for ind in population)
    families_counts_sum = sum(data_grabber.get_family_size(i) for i in range(5000))
    assert visitors_count_sum == families_counts_sum
