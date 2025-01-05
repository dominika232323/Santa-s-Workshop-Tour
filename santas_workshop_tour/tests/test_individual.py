import pytest

from santas_workshop_tour.evolutionary_algorithm import EvolutionaryAlgorithm
from santas_workshop_tour.evolutionary_algorithm import Individual
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.config import FAMILY_DATA

@pytest.fixture
def data_grabber():
    path_to_data = FAMILY_DATA
    return DataGrabber(path_to_data, sep=",")


@pytest.fixture
def individual():
    return Individual()

def test_make_preferences_dict(data_grabber, individual):
    preferences_dict = individual.make_preferences_dict(data_grabber)
    assert preferences_dict[23] == data_grabber.get_family_choices(23)
    assert preferences_dict[778] == data_grabber.get_family_choices(778)
    assert preferences_dict[3241] == data_grabber.get_family_choices(3241)