import pytest

from deap import base
from santas_workshop_tour.individual_factory import IndividualFactory
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.config import FAMILY_DATA


@pytest.fixture
def data_grabber():
    path_to_data = FAMILY_DATA
    return DataGrabber(path_to_data, sep=",")


@pytest.fixture
def factory():
    return IndividualFactory()


def test_create_toolbox(factory):
    def mock_init_func():
        return ([0, 1, 2], {1: 10, 2: 20})

    toolbox = factory.create_toolbox(mock_init_func)
    assert isinstance(toolbox, base.Toolbox)
    assert callable(toolbox.individual)


def test_init_individual(factory, data_grabber):
    visits_day, visitors_by_days = factory.init_individual(data_grabber)

    assert len(visits_day) == 5000
    assert all(0 <= day <= 100 for day in visits_day)
    assert len(visitors_by_days) == 100
    assert all(125 <= visitors < 301 for visitors in visitors_by_days.values())


def test_randomize_preferences_order(data_grabber, factory):
    original_preferences = factory.make_preferences_dict(data_grabber)
    randomized_preferences = factory.randomize_preferences_order(data_grabber)
    assert set(original_preferences) == set(randomized_preferences)

    for key in original_preferences:
        assert set(original_preferences[key]) == set(randomized_preferences[key])

    assert list(original_preferences.items()) != list(randomized_preferences.items())


def test_make_preferences_dict(data_grabber, factory):
    preferences_dict = factory.make_preferences_dict(data_grabber)
    assert preferences_dict[23] == data_grabber.get_family_choices(23)
    assert preferences_dict[778] == data_grabber.get_family_choices(778)
    assert preferences_dict[3241] == data_grabber.get_family_choices(3241)


def test_check_visiting_restriction(factory):
    visitors_by_days = {i: 0 for i in range(1, 101)}
    assert factory.check_visiting_restriction(301, 2, visitors_by_days) is False
    assert factory.check_visiting_restriction(300, 2, visitors_by_days) is True


def test_schedule_family(factory):
    visits_day = [-1 for _ in range(5000)]
    visitors_by_days = {i: 0 for i in range(1, 101)}

    visits_day, visitors_by_days = factory.schedule_family(
        family_id=10,
        day=3,
        visits_day=visits_day,
        visitors_by_days=visitors_by_days,
        family_size=4,
    )

    assert visits_day[10] == 3
    assert visitors_by_days[3] == 4


def test_verify_lower_bound(data_grabber, factory):
    visits_day = [-1 for _ in range(5000)]
    visitors_by_days = {i: 124 if i % 2 == 0 else 150 for i in range(1, 101)}

    visits_day, visitors_by_days = factory.verify_lower_bound(
        data_grabber, visits_day, visitors_by_days
    )

    assert all(visitors >= 125 for visitors in visitors_by_days.values())


def test_change_visit_day(data_grabber, factory):
    visits_day = [-1 for _ in range(5000)]
    visitors_by_days = {i: 0 for i in range(1, 101)}

    visits_day[10] = 3
    visitors_by_days[3] = 5
    family_size = data_grabber.get_family_size(10)

    visits_day, visitors_by_days = factory.change_visit_day(
        family_id=10,
        previous_day=3,
        new_day=5,
        family_choices=data_grabber,
        visits_day=visits_day,
        visitors_by_days=visitors_by_days,
    )
    previous_day_count = 5 - family_size
    assert visits_day[10] == 5
    assert visitors_by_days[3] == previous_day_count
    assert visitors_by_days[5] == family_size
