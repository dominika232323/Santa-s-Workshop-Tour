import pytest
from unittest.mock import MagicMock
from santas_workshop_tour.evolutionary_algorithm import EvolutionaryAlgorithm
from santas_workshop_tour.data_grabber import DataGrabber
from santas_workshop_tour.config import FAMILY_DATA
from santas_workshop_tour.cost_function import (
    cost_function,
    calculate_choice_penalty,
    calculate_accounting_penalty,
    calculate_restriction_penalty,
)


@pytest.fixture
def mock_data_grabber():
    mock = MagicMock()
    mock.get_family_choices.side_effect = lambda i: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    mock.get_family_size.side_effect = lambda i: (i % 5) + 1  # Family sizes between 1 and 5
    return mock


@pytest.fixture
def mock_individual():
    # [0] is the visits_day list (family ID -> chosen day)
    # [1] is the visitors_by_days dict (day -> visitor count)
    visits_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] * 500
    visitors_by_days = {i: (125 + i % 10) for i in range(1, 101)}
    return (visits_day, visitors_by_days)


@pytest.fixture
def evolutionary_algorithm():
    return EvolutionaryAlgorithm()


def test_cost_function(mock_individual, mock_data_grabber):
    visits_day = [1, 2, 3, 10, 4]
    visitors_by_days = {1: 126, 2: 134, 3: 170, 4: 128, 5: 0, 6: 0, 7: 0, 8: 0 , 9: 0, 10: 130}
    mock_individual = (visits_day, visitors_by_days)

    # Expected penalties based on manual calculation:
    # Family 0 gets day 1 (choice 0) -> penalty = 0
    # Family 1 gets day 2 (choice 0) -> penalty = 0
    # Family 2 gets day 3 (choice 0) -> penalty = 0
    # Family 3 gets day 10 (choice 4) -> penalty = 200 + family_size * 9
    # Family 4 gets day 4 (choice 3) -> penalty = 100 + family_size * 9

    mock_data_grabber.get_family_choices.side_effect = [
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 5, 6, 7],
        [1, 9, 8, 7, 10],
        [7, 5, 6, 4, 8],
    ]
    mock_data_grabber.get_family_size.side_effect = [126, 134, 170, 130, 128]  # Family sizes

    # Expected penalty calculation
    expected_choice_penalty = (
        0  # Family 0
        + 0  # Family 1
        + 0  # Family 2
        + 200
        + (130 * 9)  # Family 3 (choice 4)
        + 100
        + (128 * 9)  # Family 4 (choice 3)
    )

    expected_restriction_penalty = sum(1 for i in visitors_by_days.values() if i < 125) * 100000

    total_cost, restriction_penalty, choice_penalty, accounting_penalty = cost_function(mock_individual, mock_data_grabber)

    assert choice_penalty == expected_choice_penalty
    assert restriction_penalty == expected_restriction_penalty
    assert total_cost == (expected_restriction_penalty + expected_choice_penalty + 21162.476702791555,)


def test_calculate_restriction_penalty_lower_bound(mock_individual):
    mock_individual[1][1] -= 200
    assert calculate_restriction_penalty(mock_individual) == 100000


def test_calculate_restriction_penalty_upper_bound(mock_individual):
    mock_individual[1][1] += 200
    assert calculate_restriction_penalty(mock_individual) == 100000


def test_calculate_restriction_penalty_correct(mock_individual):
    assert calculate_restriction_penalty(mock_individual) == 0


def test_calculate_choice_penalty_chosen(mock_data_grabber):
    visits_day = [1, 2, 3, 10, 4]
    mock_individual = (visits_day, {})

    # Expected penalties based on manual calculation:
    # Family 0 gets day 1 (choice 0) -> penalty = 0
    # Family 1 gets day 2 (choice 0) -> penalty = 0
    # Family 2 gets day 3 (choice 0) -> penalty = 0
    # Family 3 gets day 10 (choice 4) -> penalty = 200 + family_size * 9
    # Family 4 gets day 4 (choice 3) -> penalty = 100 + family_size * 9

    mock_data_grabber.get_family_choices.side_effect = [
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 5, 6, 7],
        [1, 9, 8, 7, 10],
        [7, 5, 6, 4, 8],
    ]
    mock_data_grabber.get_family_size.side_effect = [3, 4, 2, 5, 6]  # Family sizes

    # Expected penalty calculation
    expected_penalty = (
        0  # Family 0
        + 0  # Family 1
        + 0  # Family 2
        + 200
        + (5 * 9)  # Family 3 (choice 4)
        + 100
        + (6 * 9)  # Family 4 (choice 3)
    )

    penalty = calculate_choice_penalty(mock_individual, mock_data_grabber)

    assert penalty == expected_penalty


def test_calculate_choice_penalty_not_chosen(mock_data_grabber):
    visits_day = [11, 12, 7, 13, 14]
    mock_individual = (visits_day, {})

    # Expected penalties based on manual calculation:
    # Family 0 gets day 1 (choice other) -> penalty = 500 + family_size * 434
    # Family 1 gets day 2 (choice other) -> penalty = 500 + family_size * 434
    # Family 2 gets day 3 (choice 4) -> penalty = 200 + family_size * 9
    # Family 3 gets day 10 (choice other) -> penalty = 500 + family_size * 434
    # Family 4 gets day 4 (choice 0) -> penalty = 0

    mock_data_grabber.get_family_choices.side_effect = [
        [1, 2, 3, 4, 5],
        [2, 3, 4, 5, 6],
        [3, 4, 5, 6, 7],
        [1, 9, 8, 7, 10],
        [14, 5, 6, 4, 8],
    ]
    mock_data_grabber.get_family_size.side_effect = [3, 4, 2, 5, 6]  # Family sizes

    # Expected penalty calculation
    expected_penalty = (
        500
        + (3 * 434)  # Family 0 (choice other)
        + 500
        + (4 * 434)  # Family 1 (choice other)
        + 200
        + (2 * 9)  # Family 2 (choice 4)
        + 500
        + (5 * 434)  # Family 3 (choice other)
        + 0  # Family 4 (choice 0)
    )

    penalty = calculate_choice_penalty(mock_individual, mock_data_grabber)

    assert penalty == expected_penalty


def test_calculate_accounting_penalty(mock_individual):
    penalty = calculate_accounting_penalty(mock_individual)

    visitors_by_days = mock_individual[1]
    prev_visitors = visitors_by_days[100]
    expected_penalty = 0
    prev_visitors_debugging_list= [prev_visitors]
    penalty_debugging_list = []
    for visitors in reversed(visitors_by_days.values()):
        temp_penalty = max(
            (visitors - 125.0) / 400.0 * visitors ** (0.5 + abs(visitors - prev_visitors) / 50.0),
            0,
        )
        penalty_debugging_list.append(temp_penalty)
        expected_penalty += temp_penalty
        prev_visitors = visitors
        prev_visitors_debugging_list.append(prev_visitors)
    assert penalty == pytest.approx(expected_penalty, rel=1e-5)
